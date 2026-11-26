"""Carga en la base de datos los usuarios y transacciones simuladas

Cada transacción se evalúa con el modelo y las reglas antes de guardarse (RN-01),
igual que en la API. Borra los datos anteriores, sirve para reiniciar la demo

Uso, desde la carpeta backend y con DATABASE_URL en el archivo .env:
    python -m scripts.seed_data
"""

from collections import defaultdict

from app.application.use_cases import assess_risk
from app.domain.entities import NewTransaction, PastTransaction, User, now_colombia
from app.infrastructure.config import get_settings
from app.infrastructure.database import connect
from app.infrastructure.ml_model import SklearnRiskModel
from scripts.data_generator import generate_dataset


def main() -> None:
    settings = get_settings()
    model = SklearnRiskModel.load(settings.model_path)
    users, transactions = generate_dataset()

    user_by_id = {u.id: User(id=u.id, name=u.name, city=u.city) for u in users}
    history: dict[int, list[PastTransaction]] = defaultdict(list)
    tx_rows, alert_rows = [], []

    for tx_id, sim in enumerate(transactions, start=1):
        tx = NewTransaction(
            user_id=sim.user_id,
            type=sim.type,
            amount=sim.amount,
            destination_account=sim.destination_account,
            city=sim.city,
            channel=sim.channel,
            created_at=sim.created_at,
        )
        result = assess_risk(model, tx, user_by_id[tx.user_id], history[tx.user_id])
        tx_rows.append((
            tx_id, tx.user_id, tx.type.value, tx.amount, tx.destination_account, tx.city,
            tx.channel.value, tx.created_at, result.risk_score, result.status.value,
        ))
        if result.needs_alert:
            alert_rows.append((tx_id, result.status.value, result.reasons, tx.created_at))
        history[tx.user_id].append(PastTransaction(tx.amount, tx.destination_account, tx.created_at))

    created = now_colombia()
    with connect() as conn, conn.transaction(), conn.cursor() as cur:
        cur.execute("TRUNCATE alerts, transactions, users RESTART IDENTITY CASCADE")
        cur.executemany(
            "INSERT INTO users (id, name, city, created_at) VALUES (%s, %s, %s, %s)",
            [(u.id, u.name, u.city, created) for u in users],
        )
        cur.executemany(
            """
            INSERT INTO transactions
                (id, user_id, type, amount, destination_account, city, channel, created_at, risk_score, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            tx_rows,
        )
        cur.executemany(
            "INSERT INTO alerts (transaction_id, level, reasons, created_at) VALUES (%s, %s, %s, %s)",
            alert_rows,
        )
        # Como los ids se insertaron a mano, se ajustan las secuencias para las nuevas filas
        for table in ("users", "transactions"):
            cur.execute(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), (SELECT MAX(id) FROM {table}))")

    statuses = defaultdict(int)
    for row in tx_rows:
        statuses[row[-1]] += 1
    print(f"Usuarios: {len(users)}")
    print(f"Transacciones: {len(tx_rows)}  aprobadas {statuses['approved']}  "
          f"en revisión {statuses['review']}  sospechosas {statuses['suspicious']}")
    print(f"Alertas: {len(alert_rows)}")


if __name__ == "__main__":
    main()
