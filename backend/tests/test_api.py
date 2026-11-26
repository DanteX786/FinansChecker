"""Pruebas de la API con repositorios en memoria, no necesitan base de datos"""

from datetime import datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.api import dependencies as deps
from app.application.use_cases import EvaluateTransaction, GetTransactionDetail
from app.domain.entities import (
    NewTransaction,
    PastTransaction,
    RiskResult,
    Transaction,
    TransactionDetail,
    User,
)
from app.main import app


class FakeUsers:
    def get(self, user_id):
        return User(id=1, name="Ana Pérez", city="Bogotá") if user_id == 1 else None

    def list_summaries(self):
        return []


class FakeTransactions:
    def __init__(self):
        self.saved = []

    def history_before(self, user_id, before):
        return [PastTransaction(Decimal("100000"), "1111111111", datetime(2026, 11, 1, 10)) for _ in range(5)]

    def save_evaluated(self, tx: NewTransaction, result: RiskResult):
        self.saved.append((tx, result))
        return Transaction(
            id=len(self.saved), user_id=tx.user_id, user_name="Ana Pérez", type=tx.type, amount=tx.amount,
            destination_account=tx.destination_account, city=tx.city, channel=tx.channel,
            created_at=tx.created_at, risk_score=result.risk_score, status=result.status,
        )

    def get_detail(self, transaction_id):
        return None


class FixedModel:
    def __init__(self, probability):
        self.probability = probability

    def predict_probability(self, features):
        return self.probability


@pytest.fixture
def client():
    repo = FakeTransactions()
    state = {"model": FixedModel(0.05)}
    app.dependency_overrides[deps.get_evaluate_transaction] = lambda: EvaluateTransaction(
        FakeUsers(), repo, state["model"]
    )
    app.dependency_overrides[deps.get_transaction_detail] = lambda: GetTransactionDetail(repo)
    with TestClient(app) as c:
        c.repo = repo
        c.state_model = state
        yield c
    app.dependency_overrides.clear()


VALID = {
    "user_id": 1,
    "type": "transfer",
    "amount": 150000,
    "destination_account": "1111111111",
    "city": "Bogotá",
    "channel": "app",
    "created_at": "2026-11-20T14:00:00",
}


def test_cp01_valid_transaction_is_saved(client):
    response = client.post("/transactions", json=VALID)
    assert response.status_code == 201
    body = response.json()
    assert body["transaction"]["status"] == "approved"
    assert 0 <= body["transaction"]["risk_score"] <= 100
    assert len(client.repo.saved) == 1


def test_suspicious_transaction_returns_reasons(client):
    client.state_model["model"] = FixedModel(0.97)
    payload = VALID | {"amount": 800000, "destination_account": "9999999999", "created_at": "2026-11-20T03:00:00"}
    body = client.post("/transactions", json=payload).json()
    assert body["transaction"]["status"] == "suspicious"
    assert body["alert_created"] is True
    assert "Monto 8,0 veces mayor a su promedio" in body["reasons"]


@pytest.mark.parametrize("amount", [-5000, 0, 50000001])
def test_invalid_amount_is_rejected_in_spanish(client, amount):
    response = client.post("/transactions", json=VALID | {"amount": amount})
    assert response.status_code == 422
    assert response.json()["errors"]["amount"] == "El monto debe estar entre $1 y $50.000.000"
    assert client.repo.saved == []


def test_invalid_account_and_type(client):
    response = client.post("/transactions", json=VALID | {"destination_account": "abc", "type": "bitcoin"})
    errors = response.json()["errors"]
    assert response.status_code == 422
    assert set(errors) == {"destination_account", "type"}


def test_future_date_is_rejected(client):
    response = client.post("/transactions", json=VALID | {"created_at": "2099-01-01T10:00:00"})
    assert response.status_code == 422
    assert "created_at" in response.json()["errors"]


def test_unknown_user_returns_404(client):
    response = client.post("/transactions", json=VALID | {"user_id": 99})
    assert response.status_code == 404
    assert response.json()["errors"]["user_id"] == "El usuario seleccionado no existe"


def test_missing_model_returns_503_without_saving(client):
    client.state_model["model"] = None
    response = client.post("/transactions", json=VALID)
    assert response.status_code == 503
    assert client.repo.saved == []


def test_unknown_transaction_returns_404(client):
    response = client.get("/transactions/12345")
    assert response.status_code == 404
    assert response.json() == {"message": "La transacción no existe"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
