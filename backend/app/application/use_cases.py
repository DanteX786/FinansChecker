"""Casos de uso de FinansChecker"""

from dataclasses import dataclass

from app.application.errors import ModelNotAvailableError, TransactionNotFoundError, UserNotFoundError
from app.application.ports import (
    AlertRepository,
    RiskModel,
    StatsRepository,
    TransactionRepository,
    UserRepository,
)
from app.domain.entities import (
    Alert,
    NewTransaction,
    PastTransaction,
    RiskResult,
    Stats,
    Status,
    Transaction,
    TransactionDetail,
    User,
    UserSummary,
)
from app.domain.features import build_features
from app.domain.risk_rules import combine


def assess_risk(model: RiskModel, tx: NewTransaction, user: User, history: list[PastTransaction]) -> RiskResult:
    """Evalúa una transacción contra el historial del usuario con el modelo y las reglas

    Se usa tanto en la API como en el script de datos de prueba, así todas las
    transacciones guardadas se evalúan con el mismo criterio (RN-01)
    """
    features = build_features(
        amount=tx.amount,
        tx_type=tx.type,
        channel=tx.channel,
        city=tx.city,
        destination_account=tx.destination_account,
        created_at=tx.created_at,
        user_city=user.city,
        history=history,
    )
    probability = model.predict_probability(features.to_vector())
    return combine(probability, features, tx.city)


@dataclass(frozen=True)
class EvaluationOutcome:
    transaction: Transaction
    result: RiskResult


class EvaluateTransaction:
    """RF-01, RF-02 y RF-03: evalúa una transacción, la guarda y crea la alerta si corresponde"""

    def __init__(self, users: UserRepository, transactions: TransactionRepository, model: RiskModel | None):
        self._users = users
        self._transactions = transactions
        self._model = model

    def execute(self, tx: NewTransaction) -> EvaluationOutcome:
        if self._model is None:
            raise ModelNotAvailableError()

        user = self._users.get(tx.user_id)
        if user is None:
            raise UserNotFoundError()

        history = self._transactions.history_before(tx.user_id, tx.created_at)
        result = assess_risk(self._model, tx, user, history)
        saved = self._transactions.save_evaluated(tx, result)
        return EvaluationOutcome(transaction=saved, result=result)


class ListTransactions:
    """RF-04: lista las transacciones de la más reciente a la más antigua"""

    def __init__(self, transactions: TransactionRepository):
        self._transactions = transactions

    def execute(self, status: Status | None = None, limit: int = 200) -> list[Transaction]:
        return self._transactions.list(status, limit)


class GetTransactionDetail:
    """RF-05: detalle de una transacción con los motivos de su alerta"""

    def __init__(self, transactions: TransactionRepository):
        self._transactions = transactions

    def execute(self, transaction_id: int) -> TransactionDetail:
        detail = self._transactions.get_detail(transaction_id)
        if detail is None:
            raise TransactionNotFoundError()
        return detail


class ListAlerts:
    """RF-03 y RF-05: alertas de transacciones en revisión o sospechosas"""

    def __init__(self, alerts: AlertRepository):
        self._alerts = alerts

    def execute(self, limit: int = 100) -> list[Alert]:
        return self._alerts.list(limit)


class GetStats:
    """RF-06: resumen de la actividad para el dashboard"""

    def __init__(self, stats: StatsRepository):
        self._stats = stats

    def execute(self, days: int = 14) -> Stats:
        return self._stats.get_stats(days)


class ListUsers:
    """Usuarios de prueba disponibles en el simulador"""

    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self) -> list[UserSummary]:
        return self._users.list_summaries()
