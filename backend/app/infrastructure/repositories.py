"""Repositorios con psycopg y SQL directo, todas las consultas usan parámetros"""

from datetime import datetime, timedelta

import psycopg

from app.domain.entities import (
    Alert,
    Channel,
    DayCount,
    NewTransaction,
    PastTransaction,
    RiskResult,
    Stats,
    Status,
    Transaction,
    TransactionDetail,
    TransactionType,
    User,
    UserSummary,
    now_colombia,
)

TRANSACTION_COLUMNS = """
    t.id, t.user_id, u.name AS user_name, u.city AS user_city, t.type, t.amount,
    t.destination_account, t.city, t.channel, t.created_at, t.risk_score, t.status
"""


def _to_transaction(row: dict) -> Transaction:
    return Transaction(
        id=row["id"],
        user_id=row["user_id"],
        user_name=row["user_name"],
        type=TransactionType(row["type"]),
        amount=row["amount"],
        destination_account=row["destination_account"],
        city=row["city"],
        channel=Channel(row["channel"]),
        created_at=row["created_at"],
        risk_score=row["risk_score"],
        status=Status(row["status"]),
    )


class PostgresUserRepository:
    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    def get(self, user_id: int) -> User | None:
        row = self._conn.execute("SELECT id, name, city FROM users WHERE id = %s", (user_id,)).fetchone()
        return User(**row) if row else None

    def list_summaries(self) -> list[UserSummary]:
        rows = self._conn.execute(
            """
            SELECT u.id, u.name, u.city,
                   COALESCE(ROUND(AVG(t.amount), 2), 0) AS average_amount,
                   COUNT(t.id) AS transaction_count,
                   (SELECT t2.destination_account
                      FROM transactions t2
                     WHERE t2.user_id = u.id
                     GROUP BY t2.destination_account
                     ORDER BY COUNT(*) DESC, t2.destination_account
                     LIMIT 1) AS usual_destination
              FROM users u
              LEFT JOIN transactions t ON t.user_id = u.id
             GROUP BY u.id
             ORDER BY u.name
            """
        ).fetchall()
        return [UserSummary(**row) for row in rows]


class PostgresTransactionRepository:
    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    def history_before(self, user_id: int, before: datetime) -> list[PastTransaction]:
        rows = self._conn.execute(
            """
            SELECT amount, destination_account, created_at
              FROM transactions
             WHERE user_id = %s AND created_at <= %s
             ORDER BY created_at
            """,
            (user_id, before),
        ).fetchall()
        return [PastTransaction(**row) for row in rows]

    def save_evaluated(self, tx: NewTransaction, result: RiskResult) -> Transaction:
        # La transacción y su alerta se guardan juntas o no se guarda ninguna
        with self._conn.transaction():
            row = self._conn.execute(
                """
                INSERT INTO transactions
                    (user_id, type, amount, destination_account, city, channel, created_at, risk_score, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    tx.user_id,
                    tx.type.value,
                    tx.amount,
                    tx.destination_account,
                    tx.city,
                    tx.channel.value,
                    tx.created_at,
                    result.risk_score,
                    result.status.value,
                ),
            ).fetchone()
            if result.needs_alert:
                self._conn.execute(
                    "INSERT INTO alerts (transaction_id, level, reasons, created_at) VALUES (%s, %s, %s, %s)",
                    (row["id"], result.status.value, result.reasons, tx.created_at),
                )
        detail = self.get_detail(row["id"])
        return detail.transaction

    def list(self, status: Status | None, limit: int) -> list[Transaction]:
        rows = self._conn.execute(
            f"""
            SELECT {TRANSACTION_COLUMNS}
              FROM transactions t
              JOIN users u ON u.id = t.user_id
             WHERE (%(status)s::varchar IS NULL OR t.status = %(status)s)
             ORDER BY t.created_at DESC, t.id DESC
             LIMIT %(limit)s
            """,
            {"status": status.value if status else None, "limit": limit},
        ).fetchall()
        return [_to_transaction(row) for row in rows]

    def get_detail(self, transaction_id: int) -> TransactionDetail | None:
        row = self._conn.execute(
            f"""
            SELECT {TRANSACTION_COLUMNS}, a.reasons
              FROM transactions t
              JOIN users u ON u.id = t.user_id
              LEFT JOIN alerts a ON a.transaction_id = t.id
             WHERE t.id = %s
            """,
            (transaction_id,),
        ).fetchone()
        if row is None:
            return None
        return TransactionDetail(
            transaction=_to_transaction(row),
            user_city=row["user_city"],
            reasons=row["reasons"] or [],
        )


class PostgresAlertRepository:
    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    def list(self, limit: int) -> list[Alert]:
        rows = self._conn.execute(
            """
            SELECT a.id, a.transaction_id, a.level, a.reasons, a.created_at,
                   u.name AS user_name, t.amount, t.type, t.risk_score
              FROM alerts a
              JOIN transactions t ON t.id = a.transaction_id
              JOIN users u ON u.id = t.user_id
             ORDER BY a.created_at DESC, a.id DESC
             LIMIT %s
            """,
            (limit,),
        ).fetchall()
        return [
            Alert(
                id=row["id"],
                transaction_id=row["transaction_id"],
                level=Status(row["level"]),
                reasons=row["reasons"],
                created_at=row["created_at"],
                user_name=row["user_name"],
                amount=row["amount"],
                type=TransactionType(row["type"]),
                risk_score=row["risk_score"],
            )
            for row in rows
        ]


class PostgresStatsRepository:
    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    def get_stats(self, days: int) -> Stats:
        totals = self._conn.execute(
            """
            SELECT COUNT(*) AS total,
                   COALESCE(SUM(amount), 0) AS total_amount,
                   COUNT(*) FILTER (WHERE status = 'approved') AS approved,
                   COUNT(*) FILTER (WHERE status = 'review') AS review,
                   COUNT(*) FILTER (WHERE status = 'suspicious') AS suspicious,
                   (SELECT COUNT(*) FROM alerts) AS alerts
              FROM transactions
            """
        ).fetchone()

        # La fecha de hoy se calcula en hora de Colombia, no en la del servidor de Neon
        today = now_colombia().date()
        start = today - timedelta(days=days - 1)
        rows = self._conn.execute(
            """
            SELECT d::date AS day,
                   COUNT(t.id) FILTER (WHERE t.status = 'approved') AS approved,
                   COUNT(t.id) FILTER (WHERE t.status = 'review') AS review,
                   COUNT(t.id) FILTER (WHERE t.status = 'suspicious') AS suspicious
              FROM generate_series(%s::date, %s::date, interval '1 day') AS d
              LEFT JOIN transactions t ON t.created_at::date = d::date
             GROUP BY d
             ORDER BY d
            """,
            (start, today),
        ).fetchall()

        return Stats(
            total_transactions=totals["total"],
            total_amount=totals["total_amount"],
            approved_count=totals["approved"],
            review_count=totals["review"],
            suspicious_count=totals["suspicious"],
            alert_count=totals["alerts"],
            by_day=[
                DayCount(
                    day=row["day"].isoformat(),
                    approved=row["approved"],
                    review=row["review"],
                    suspicious=row["suspicious"],
                )
                for row in rows
            ],
        )
