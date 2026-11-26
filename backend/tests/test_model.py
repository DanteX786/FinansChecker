"""Pruebas del motor de riesgo completo con el modelo entrenado (CP-02)"""

from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from app.application.use_cases import assess_risk
from app.domain.entities import Channel, NewTransaction, PastTransaction, Status, TransactionType, User
from app.infrastructure.config import get_settings
from app.infrastructure.ml_model import SklearnRiskModel

BASE = datetime(2026, 11, 20, 15, 0)
USER = User(id=1, name="Usuario de prueba", city="Medellín")


@pytest.fixture(scope="module")
def model():
    return SklearnRiskModel.load(get_settings().model_path)


@pytest.fixture
def history():
    # Historial habitual: unos 100 mil pesos a tres cuentas conocidas en horario diurno
    accounts = ["1234567890", "2345678901", "3456789012"]
    return [
        PastTransaction(Decimal(90000 + (i % 5) * 5000), accounts[i % 3], BASE - timedelta(days=i + 1, hours=i % 6))
        for i in range(30)
    ]


def tx(amount, destination, when, city="Medellín"):
    return NewTransaction(
        user_id=1,
        type=TransactionType.TRANSFER,
        amount=Decimal(amount),
        destination_account=destination,
        city=city,
        channel=Channel.APP,
        created_at=when,
    )


def test_model_metrics_are_saved(model):
    assert model.metrics["combined_recall"] > 0.8


def test_cp02_suspicious_transaction(model, history):
    # CP-02: monto 8 veces mayor al promedio, a las 3:00 a. m., a una cuenta nueva
    average = sum(float(h.amount) for h in history) / len(history)
    result = assess_risk(model, tx(round(average * 8), "9876543210", BASE.replace(hour=3)), USER, history)
    assert 70 <= result.risk_score <= 100
    assert result.status == Status.SUSPICIOUS
    assert len(result.reasons) >= 1


def test_usual_transaction_is_approved(model, history):
    result = assess_risk(model, tx(100000, "1234567890", BASE), USER, history)
    assert result.risk_score < 40
    assert result.status == Status.APPROVED
