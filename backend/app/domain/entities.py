"""Entidades del dominio de FinansChecker

Este módulo no depende de FastAPI, psycopg ni scikit-learn, solo de Python estándar
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from enum import Enum

# Colombia no tiene horario de verano, por eso basta un desfase fijo de UTC-5
COLOMBIA_TZ = timezone(timedelta(hours=-5))

MIN_AMOUNT = Decimal("1")
MAX_AMOUNT = Decimal("50000000")


class TransactionType(str, Enum):
    TRANSFER = "transfer"
    PAYMENT = "payment"
    WITHDRAWAL = "withdrawal"
    ONLINE_PURCHASE = "online_purchase"


class Channel(str, Enum):
    APP = "app"
    WEB = "web"
    ATM = "atm"


class Status(str, Enum):
    APPROVED = "approved"
    REVIEW = "review"
    SUSPICIOUS = "suspicious"


def now_colombia() -> datetime:
    """Hora actual de Colombia sin zona horaria, que es como se guarda en la base de datos"""
    return datetime.now(COLOMBIA_TZ).replace(tzinfo=None, microsecond=0)


@dataclass(frozen=True)
class User:
    id: int
    name: str
    city: str


@dataclass(frozen=True)
class UserSummary:
    id: int
    name: str
    city: str
    average_amount: Decimal
    transaction_count: int
    usual_destination: str | None


@dataclass(frozen=True)
class NewTransaction:
    """Transacción que llega del simulador y todavía no ha sido evaluada"""

    user_id: int
    type: TransactionType
    amount: Decimal
    destination_account: str
    city: str
    channel: Channel
    created_at: datetime


@dataclass(frozen=True)
class PastTransaction:
    """Lo mínimo del historial que necesita el motor de riesgo"""

    amount: Decimal
    destination_account: str
    created_at: datetime


@dataclass(frozen=True)
class RiskResult:
    risk_score: int
    status: Status
    reasons: list[str] = field(default_factory=list)
    model_score: int = 0
    rules_score: int = 0

    @property
    def needs_alert(self) -> bool:
        return self.status in (Status.REVIEW, Status.SUSPICIOUS)


@dataclass(frozen=True)
class Transaction:
    id: int
    user_id: int
    user_name: str
    type: TransactionType
    amount: Decimal
    destination_account: str
    city: str
    channel: Channel
    created_at: datetime
    risk_score: int
    status: Status


@dataclass(frozen=True)
class TransactionDetail:
    transaction: Transaction
    user_city: str
    reasons: list[str]


@dataclass(frozen=True)
class Alert:
    id: int
    transaction_id: int
    level: Status
    reasons: list[str]
    created_at: datetime
    user_name: str
    amount: Decimal
    type: TransactionType
    risk_score: int


@dataclass(frozen=True)
class DayCount:
    day: str
    approved: int
    review: int
    suspicious: int


@dataclass(frozen=True)
class Stats:
    total_transactions: int
    total_amount: Decimal
    approved_count: int
    review_count: int
    suspicious_count: int
    alert_count: int
    by_day: list[DayCount]

    @property
    def suspicious_percentage(self) -> float:
        if self.total_transactions == 0:
            return 0.0
        return round(self.suspicious_count * 100 / self.total_transactions, 1)
