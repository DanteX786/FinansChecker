"""Interfaces que la capa de infraestructura debe implementar

Los casos de uso dependen de estas interfaces y no de psycopg ni de scikit-learn
"""

from datetime import datetime
from typing import Protocol

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


class RiskModel(Protocol):
    def predict_probability(self, features: list[float]) -> float:
        """Probabilidad de fraude entre 0 y 1"""
        ...


class UserRepository(Protocol):
    def get(self, user_id: int) -> User | None: ...

    def list_summaries(self) -> list[UserSummary]: ...


class TransactionRepository(Protocol):
    def history_before(self, user_id: int, before: datetime) -> list[PastTransaction]: ...

    def save_evaluated(self, tx: NewTransaction, result: RiskResult) -> Transaction:
        """Guarda la transacción ya evaluada y, si corresponde, su alerta en una sola operación"""
        ...

    def list(self, status: Status | None, limit: int) -> list[Transaction]: ...

    def get_detail(self, transaction_id: int) -> TransactionDetail | None: ...


class AlertRepository(Protocol):
    def list(self, limit: int) -> list[Alert]: ...


class StatsRepository(Protocol):
    def get_stats(self, days: int) -> Stats: ...
