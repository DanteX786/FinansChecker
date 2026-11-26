"""Pruebas unitarias del dominio, no necesitan base de datos"""

from datetime import datetime, timedelta
from decimal import Decimal

from app.domain.entities import Channel, PastTransaction, Status, TransactionType
from app.domain.features import build_features
from app.domain.risk_rules import MODEL_ONLY_REASON, combine, evaluate_rules, status_from_score

BASE = datetime(2026, 11, 20, 14, 0)


def history(amount="100000", destination="1111111111", count=10):
    return [
        PastTransaction(Decimal(amount), destination, BASE - timedelta(days=i + 1))
        for i in range(count)
    ]


def features(amount="100000", destination="1111111111", city="Bogotá", when=BASE, past=None):
    return build_features(
        amount=Decimal(amount),
        tx_type=TransactionType.TRANSFER,
        channel=Channel.APP,
        city=city,
        destination_account=destination,
        created_at=when,
        user_city="Bogotá",
        history=history() if past is None else past,
    )


def test_status_thresholds_rn02():
    assert status_from_score(0) == Status.APPROVED
    assert status_from_score(39) == Status.APPROVED
    assert status_from_score(40) == Status.REVIEW
    assert status_from_score(69) == Status.REVIEW
    assert status_from_score(70) == Status.SUSPICIOUS
    assert status_from_score(100) == Status.SUSPICIOUS


def test_normal_transaction_has_no_reasons():
    points, reasons = evaluate_rules(features(), "Bogotá")
    assert points == 0
    assert reasons == []


def test_amount_more_than_five_times_average():
    points, reasons = evaluate_rules(features(amount="800000"), "Bogotá")
    assert points > 0
    assert reasons == ["Monto 8,0 veces mayor a su promedio"]


def test_amount_exactly_five_times_is_not_flagged():
    _, reasons = evaluate_rules(features(amount="500000"), "Bogotá")
    assert reasons == []


def test_night_time_between_midnight_and_five():
    _, at_3am = evaluate_rules(features(when=BASE.replace(hour=3)), "Bogotá")
    _, at_5am = evaluate_rules(features(when=BASE.replace(hour=5)), "Bogotá")
    assert at_3am == ["Transacción de madrugada (entre 12 y 5 a. m.)"]
    assert at_5am == []


def test_three_transactions_in_ten_minutes():
    past = history() + [
        PastTransaction(Decimal("100000"), "1111111111", BASE - timedelta(minutes=4)),
        PastTransaction(Decimal("100000"), "1111111111", BASE - timedelta(minutes=8)),
    ]
    _, reasons = evaluate_rules(features(past=past), "Bogotá")
    assert reasons == ["3 transacciones en menos de 10 minutos"]


def test_new_destination_and_different_city():
    _, reasons = evaluate_rules(features(destination="9999999999", city="Cali"), "Cali")
    assert reasons == ["Cuenta destino nueva para el usuario", "Ciudad distinta a la habitual (Cali)"]


def test_user_without_history_is_not_penalized():
    _, reasons = evaluate_rules(features(destination="9999999999", past=[]), "Bogotá")
    assert reasons == []


def test_combined_score_never_exceeds_100():
    f = features(amount="5000000", destination="9999999999", city="Cali", when=BASE.replace(hour=2))
    result = combine(1.0, f, "Cali")
    assert result.risk_score == 100
    assert result.status == Status.SUSPICIOUS


def test_alert_always_has_a_reason_rn02():
    # El modelo marca riesgo alto pero ninguna regla se activa
    result = combine(0.95, features(), "Bogotá")
    assert result.status == Status.REVIEW
    assert result.reasons == [MODEL_ONLY_REASON]


def test_approved_low_score():
    result = combine(0.02, features(), "Bogotá")
    assert result.status == Status.APPROVED
    assert result.risk_score < 40
