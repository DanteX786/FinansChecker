"""Esquemas de Pydantic, validan lo que entra y dan forma a lo que sale de la API"""

from datetime import datetime, timedelta
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.domain.entities import (
    MAX_AMOUNT,
    MIN_AMOUNT,
    Alert,
    Channel,
    DayCount,
    Stats,
    Status,
    Transaction,
    TransactionDetail,
    TransactionType,
    UserSummary,
    now_colombia,
)

# Mensajes en español que se devuelven por campo cuando la validación falla
FIELD_MESSAGES = {
    "user_id": "Selecciona un usuario válido",
    "type": "Selecciona un tipo de transacción válido",
    "amount": "El monto debe estar entre $1 y $50.000.000",
    "destination_account": "La cuenta destino debe tener entre 6 y 20 dígitos",
    "city": "Escribe una ciudad válida",
    "channel": "Selecciona un canal válido",
    "created_at": "La fecha no es válida o está en el futuro",
}


class TransactionCreate(BaseModel):
    user_id: int = Field(gt=0)
    type: TransactionType
    amount: Decimal = Field(ge=MIN_AMOUNT, le=MAX_AMOUNT, decimal_places=2)
    destination_account: str = Field(pattern=r"^\d{6,20}$")
    city: str = Field(min_length=2, max_length=60)
    channel: Channel
    created_at: datetime | None = Field(
        default=None,
        description="Fecha y hora opcional para pruebas, si no se envía se usa la hora actual de Colombia",
    )

    @field_validator("destination_account", "city", mode="before")
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("created_at")
    @classmethod
    def not_in_future(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        value = value.replace(tzinfo=None, microsecond=0)
        if value > now_colombia() + timedelta(minutes=5) or value.year < 2020:
            raise ValueError("fecha inválida")
        return value


class UserOut(BaseModel):
    id: int
    name: str
    city: str
    average_amount: float
    transaction_count: int
    usual_destination: str | None

    @classmethod
    def from_domain(cls, user: UserSummary) -> "UserOut":
        return cls(
            id=user.id,
            name=user.name,
            city=user.city,
            average_amount=float(user.average_amount),
            transaction_count=user.transaction_count,
            usual_destination=user.usual_destination,
        )


class TransactionOut(BaseModel):
    id: int
    user_id: int
    user_name: str
    type: TransactionType
    amount: float
    destination_account: str
    city: str
    channel: Channel
    created_at: datetime
    risk_score: int
    status: Status

    @classmethod
    def from_domain(cls, tx: Transaction) -> "TransactionOut":
        return cls(
            id=tx.id,
            user_id=tx.user_id,
            user_name=tx.user_name,
            type=tx.type,
            amount=float(tx.amount),
            destination_account=tx.destination_account,
            city=tx.city,
            channel=tx.channel,
            created_at=tx.created_at,
            risk_score=tx.risk_score,
            status=tx.status,
        )


class EvaluationOut(BaseModel):
    transaction: TransactionOut
    reasons: list[str]
    alert_created: bool


class TransactionDetailOut(BaseModel):
    transaction: TransactionOut
    user_city: str
    reasons: list[str]

    @classmethod
    def from_domain(cls, detail: TransactionDetail) -> "TransactionDetailOut":
        return cls(
            transaction=TransactionOut.from_domain(detail.transaction),
            user_city=detail.user_city,
            reasons=detail.reasons,
        )


class AlertOut(BaseModel):
    id: int
    transaction_id: int
    level: Status
    reasons: list[str]
    created_at: datetime
    user_name: str
    amount: float
    type: TransactionType
    risk_score: int

    @classmethod
    def from_domain(cls, alert: Alert) -> "AlertOut":
        return cls(
            id=alert.id,
            transaction_id=alert.transaction_id,
            level=alert.level,
            reasons=alert.reasons,
            created_at=alert.created_at,
            user_name=alert.user_name,
            amount=float(alert.amount),
            type=alert.type,
            risk_score=alert.risk_score,
        )


class DayCountOut(BaseModel):
    day: str
    approved: int
    review: int
    suspicious: int

    @classmethod
    def from_domain(cls, item: DayCount) -> "DayCountOut":
        return cls(day=item.day, approved=item.approved, review=item.review, suspicious=item.suspicious)


class StatsOut(BaseModel):
    total_transactions: int
    total_amount: float
    approved_count: int
    review_count: int
    suspicious_count: int
    suspicious_percentage: float
    alert_count: int
    by_day: list[DayCountOut]

    @classmethod
    def from_domain(cls, stats: Stats) -> "StatsOut":
        return cls(
            total_transactions=stats.total_transactions,
            total_amount=float(stats.total_amount),
            approved_count=stats.approved_count,
            review_count=stats.review_count,
            suspicious_count=stats.suspicious_count,
            suspicious_percentage=stats.suspicious_percentage,
            alert_count=stats.alert_count,
            by_day=[DayCountOut.from_domain(d) for d in stats.by_day],
        )


class HealthOut(BaseModel):
    status: str
    model_loaded: bool
