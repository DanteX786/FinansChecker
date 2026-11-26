"""Genera usuarios y transacciones simuladas con Faker, incluidos casos de fraude

Todo es ficticio, la misma semilla produce siempre los mismos datos, así el
entrenamiento del modelo y la carga en Neon usan exactamente el mismo conjunto
"""

import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal

from faker import Faker

from app.domain.entities import Channel, TransactionType, now_colombia

CITIES = [
    "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
    "Bucaramanga", "Pereira", "Manizales", "Santa Marta", "Cúcuta",
]

DEFAULT_SEED = 42


@dataclass
class SimUser:
    id: int
    name: str
    city: str
    own_account: str
    base_amount: float
    daily_rate: float
    frequent_destinations: list[str] = field(default_factory=list)


@dataclass
class SimTransaction:
    user_id: int
    type: TransactionType
    amount: Decimal
    destination_account: str
    city: str
    channel: Channel
    created_at: datetime
    is_fraud: bool


def _account(rng: random.Random) -> str:
    return "".join(str(rng.randint(0, 9)) for _ in range(10))


def _round_cop(value: float) -> Decimal:
    # Los montos en pesos se redondean a centenas y se mantienen dentro del límite de RN-03
    value = max(1000.0, min(value, 49_000_000.0))
    return Decimal(int(round(value / 100.0)) * 100)


def _channel_for(tx_type: TransactionType, rng: random.Random) -> Channel:
    if tx_type == TransactionType.WITHDRAWAL:
        return Channel.ATM
    return rng.choices([Channel.APP, Channel.WEB], weights=[0.7, 0.3])[0]


def _other_city(home: str, rng: random.Random) -> str:
    return rng.choice([c for c in CITIES if c != home])


def generate_users(count: int, rng: random.Random, faker: Faker) -> list[SimUser]:
    users = []
    for user_id in range(1, count + 1):
        users.append(
            SimUser(
                id=user_id,
                name=f"{faker.first_name()} {faker.last_name()} {faker.last_name()}",
                city=rng.choice(CITIES),
                own_account=_account(rng),
                # Cada usuario tiene su propio nivel de gasto, entre unos 40 mil y 600 mil pesos
                base_amount=math.exp(rng.uniform(math.log(40_000), math.log(600_000))),
                daily_rate=rng.uniform(0.5, 1.3),
                frequent_destinations=[_account(rng) for _ in range(rng.randint(3, 6))],
            )
        )
    return users


def _normal_transaction(user: SimUser, when: datetime, rng: random.Random) -> SimTransaction:
    tx_type = rng.choices(list(TransactionType), weights=[0.35, 0.3, 0.15, 0.2])[0]
    if tx_type == TransactionType.WITHDRAWAL:
        destination = user.own_account
    elif rng.random() < 0.88:
        destination = rng.choice(user.frequent_destinations)
    else:
        # A veces una persona sí paga a una cuenta nueva sin que sea fraude
        destination = _account(rng)
    city = user.city if rng.random() < 0.95 else _other_city(user.city, rng)
    amount = user.base_amount * rng.lognormvariate(0, 0.45)
    return SimTransaction(
        user_id=user.id,
        type=tx_type,
        amount=_round_cop(amount),
        destination_account=destination,
        city=city,
        channel=_channel_for(tx_type, rng),
        created_at=when,
        is_fraud=False,
    )


def _fraud_transactions(user: SimUser, day: datetime, rng: random.Random) -> list[SimTransaction]:
    """Crea uno de cuatro patrones de fraude típicos para un usuario en un día dado"""
    pattern = rng.choice(["night_big", "burst", "takeover", "big_new"])
    new_destination = _account(rng)
    base = user.base_amount
    txs: list[SimTransaction] = []

    def make(when: datetime, amount: float, tx_type: TransactionType, city: str) -> SimTransaction:
        return SimTransaction(
            user_id=user.id,
            type=tx_type,
            amount=_round_cop(amount),
            destination_account=new_destination,
            city=city,
            channel=_channel_for(tx_type, rng),
            created_at=when,
            is_fraud=True,
        )

    if pattern == "night_big":
        when = day.replace(hour=rng.randint(0, 4), minute=rng.randint(0, 59))
        city = user.city if rng.random() < 0.5 else _other_city(user.city, rng)
        txs.append(make(when, base * rng.uniform(6, 15), TransactionType.TRANSFER, city))
    elif pattern == "burst":
        hour = rng.randint(0, 4) if rng.random() < 0.4 else rng.randint(8, 22)
        start = day.replace(hour=hour, minute=rng.randint(0, 45))
        for i in range(rng.randint(3, 5)):
            when = start + timedelta(minutes=i * rng.randint(1, 3))
            txs.append(make(when, base * rng.uniform(1.5, 4), TransactionType.ONLINE_PURCHASE, user.city))
    elif pattern == "takeover":
        when = day.replace(hour=rng.randint(9, 21), minute=rng.randint(0, 59))
        txs.append(make(when, base * rng.uniform(3, 8), TransactionType.TRANSFER, _other_city(user.city, rng)))
    else:
        when = day.replace(hour=rng.randint(8, 22), minute=rng.randint(0, 59))
        txs.append(make(when, base * rng.uniform(6, 12), TransactionType.TRANSFER, user.city))
    return txs


def generate_dataset(
    user_count: int = 30,
    days: int = 45,
    fraud_rate: float = 0.05,
    seed: int = DEFAULT_SEED,
    end: datetime | None = None,
) -> tuple[list[SimUser], list[SimTransaction]]:
    """Devuelve usuarios y transacciones ordenadas por fecha, ninguna en el futuro"""
    rng = random.Random(seed)
    faker = Faker("es_CO")
    faker.seed_instance(seed)

    end = end or now_colombia()
    start_day = (end - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
    users = generate_users(user_count, rng, faker)
    transactions: list[SimTransaction] = []

    for user in users:
        # Los primeros días solo hay movimientos normales para que cada usuario tenga historial
        for offset in range(days + 1):
            day = start_day + timedelta(days=offset)
            count = sum(1 for _ in range(3) if rng.random() < user.daily_rate / 3)
            for _ in range(count):
                if rng.random() < 0.02:
                    hour = rng.randint(0, 5)  # pocas transacciones legítimas de madrugada
                else:
                    hour = rng.randint(7, 22)
                when = day.replace(hour=hour, minute=rng.randint(0, 59), second=rng.randint(0, 59))
                transactions.append(_normal_transaction(user, when, rng))

            if offset >= 7 and rng.random() < fraud_rate:
                transactions.extend(_fraud_transactions(user, day, rng))

    transactions = [t for t in transactions if t.created_at <= end]
    transactions.sort(key=lambda t: (t.created_at, t.user_id))
    return users, transactions
