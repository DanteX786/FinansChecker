"""Cálculo de las variables que usan el modelo de IA y las reglas

El mismo cálculo se usa al entrenar el modelo y al evaluar transacciones en la API,
así el modelo siempre recibe los datos de la misma forma
"""

import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from app.domain.entities import Channel, PastTransaction, TransactionType

RECENT_WINDOW = timedelta(minutes=10)

TYPE_CODES = {t: i for i, t in enumerate(TransactionType)}
CHANNEL_CODES = {c: i for i, c in enumerate(Channel)}

FEATURE_NAMES = [
    "amount_ratio",
    "log_amount",
    "hour",
    "is_night",
    "recent_count",
    "is_new_destination",
    "is_different_city",
    "type_code",
    "channel_code",
]


@dataclass(frozen=True)
class TransactionFeatures:
    amount_ratio: float
    average_amount: float
    log_amount: float
    hour: int
    is_night: bool
    recent_count: int
    is_new_destination: bool
    is_different_city: bool
    type_code: int
    channel_code: int

    def to_vector(self) -> list[float]:
        return [
            self.amount_ratio,
            self.log_amount,
            float(self.hour),
            float(self.is_night),
            float(self.recent_count),
            float(self.is_new_destination),
            float(self.is_different_city),
            float(self.type_code),
            float(self.channel_code),
        ]


def build_features(
    amount: Decimal,
    tx_type: TransactionType,
    channel: Channel,
    city: str,
    destination_account: str,
    created_at: datetime,
    user_city: str,
    history: list[PastTransaction],
) -> TransactionFeatures:
    """Calcula las variables de una transacción comparándola con el historial del usuario

    El historial solo debe incluir transacciones anteriores a created_at
    """
    amount_value = float(amount)

    if history:
        average = sum(float(t.amount) for t in history) / len(history)
    else:
        # Sin historial no hay contra qué comparar, se asume un monto normal
        average = amount_value
    ratio = amount_value / average if average > 0 else 1.0

    # Se cuenta la transacción actual más las anteriores dentro de la ventana de 10 minutos
    recent = 1 + sum(1 for t in history if created_at - RECENT_WINDOW <= t.created_at <= created_at)

    known_destinations = {t.destination_account for t in history}
    # Un usuario sin historial no tiene destinos conocidos, pero tampoco es sospechoso por eso
    is_new_destination = bool(history) and destination_account not in known_destinations

    return TransactionFeatures(
        amount_ratio=round(ratio, 4),
        average_amount=round(average, 2),
        log_amount=round(math.log10(max(amount_value, 1.0)), 4),
        hour=created_at.hour,
        is_night=0 <= created_at.hour < 5,
        recent_count=recent,
        is_new_destination=is_new_destination,
        is_different_city=city.strip().lower() != user_city.strip().lower(),
        type_code=TYPE_CODES[tx_type],
        channel_code=CHANNEL_CODES[channel],
    )
