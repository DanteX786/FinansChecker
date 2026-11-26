"""Prueba de integración con una base de datos real

Solo se ejecuta si existe la variable TEST_DATABASE_URL, apuntando a una base con
schema.sql aplicado y los datos de seed_data.py cargados. No usar la base de producción
"""

import os

import pytest
from fastapi.testclient import TestClient

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not TEST_DATABASE_URL, reason="TEST_DATABASE_URL no está definida")


@pytest.fixture(scope="module")
def client():
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    from app.main import app

    with TestClient(app) as c:
        yield c


def test_full_flow_cp01_cp02_and_dashboard(client):
    users = client.get("/users").json()
    assert users, "Primero ejecuta scripts/seed_data.py"
    user = users[0]
    before = client.get("/stats").json()

    # CP-01: transacción normal
    normal = client.post("/transactions", json={
        "user_id": user["id"], "type": "transfer", "amount": 150000,
        "destination_account": user["usual_destination"], "city": user["city"], "channel": "app",
    })
    assert normal.status_code == 201

    # CP-02: monto 8 veces mayor al promedio, 3:00 a. m., cuenta nueva
    from datetime import timedelta

    from app.domain.entities import now_colombia
    at_3am = (now_colombia() - timedelta(days=1)).replace(hour=3, minute=0, second=0)
    suspicious = client.post("/transactions", json={
        "user_id": user["id"], "type": "transfer", "amount": round(user["average_amount"] * 8),
        "destination_account": "5550001112", "city": user["city"], "channel": "app",
        "created_at": at_3am.isoformat(),
    }).json()
    assert suspicious["transaction"]["status"] == "suspicious"
    assert 70 <= suspicious["transaction"]["risk_score"] <= 100

    # La alerta aparece en Alertas y el detalle trae sus motivos (RF-03, RF-05)
    alerts = client.get("/alerts").json()
    assert any(a["transaction_id"] == suspicious["transaction"]["id"] for a in alerts)
    detail = client.get(f"/transactions/{suspicious['transaction']['id']}").json()
    assert detail["reasons"]

    # CA-03: el dashboard se actualiza
    after = client.get("/stats").json()
    assert after["total_transactions"] == before["total_transactions"] + 2
    assert after["suspicious_count"] == before["suspicious_count"] + 1

    # RF-04: filtro por estado
    only_suspicious = client.get("/transactions", params={"status": "suspicious"}).json()
    assert all(t["status"] == "suspicious" for t in only_suspicious)
