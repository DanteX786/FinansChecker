"""Reglas de negocio del motor de riesgo (RN-01, RN-02 y RN-03)"""

from app.domain.entities import RiskResult, Status
from app.domain.features import TransactionFeatures

# Umbrales de RN-03
AMOUNT_RATIO_THRESHOLD = 5.0
RECENT_COUNT_THRESHOLD = 3

# Puntos que suma cada regla, el total se limita a 100
# Se eligieron para que un caso como CP-02 (monto alto, madrugada y destino nuevo)
# quede sospechoso aunque el modelo dude, y una sola señal leve no baste para alertar
RULE_POINTS = {
    "high_amount": 40,
    "rapid_transactions": 35,
    "night_time": 25,
    "new_destination": 20,
    "different_city": 15,
}

# El puntaje final pesa por igual la opinión del modelo y la de las reglas
MODEL_WEIGHT = 0.5
RULES_WEIGHT = 0.5

REVIEW_THRESHOLD = 40
SUSPICIOUS_THRESHOLD = 70

MODEL_ONLY_REASON = "El modelo de IA detectó un patrón inusual frente al historial del usuario"


def evaluate_rules(features: TransactionFeatures, city: str) -> tuple[int, list[str]]:
    """Aplica las reglas de RN-03 y devuelve los puntos acumulados y los motivos en español"""
    points = 0
    reasons: list[str] = []

    if features.amount_ratio > AMOUNT_RATIO_THRESHOLD:
        points += RULE_POINTS["high_amount"]
        ratio = f"{features.amount_ratio:.1f}".replace(".", ",")
        reasons.append(f"Monto {ratio} veces mayor a su promedio")

    if features.recent_count >= RECENT_COUNT_THRESHOLD:
        points += RULE_POINTS["rapid_transactions"]
        reasons.append(f"{features.recent_count} transacciones en menos de 10 minutos")

    if features.is_night:
        points += RULE_POINTS["night_time"]
        reasons.append("Transacción de madrugada (entre 12 y 5 a. m.)")

    if features.is_new_destination:
        points += RULE_POINTS["new_destination"]
        reasons.append("Cuenta destino nueva para el usuario")

    if features.is_different_city:
        points += RULE_POINTS["different_city"]
        reasons.append(f"Ciudad distinta a la habitual ({city})")

    return min(points, 100), reasons


def status_from_score(score: int) -> Status:
    """RN-02: 0 a 39 aprobada, 40 a 69 en revisión, 70 a 100 sospechosa"""
    if score >= SUSPICIOUS_THRESHOLD:
        return Status.SUSPICIOUS
    if score >= REVIEW_THRESHOLD:
        return Status.REVIEW
    return Status.APPROVED


def combine(model_probability: float, features: TransactionFeatures, city: str) -> RiskResult:
    """RN-01: combina el modelo de IA y las reglas en un puntaje de 0 a 100

    Si la transacción queda en revisión o sospechosa sin que ninguna regla se active,
    se agrega el motivo del modelo, porque RN-02 exige al menos un motivo por alerta
    """
    model_score = round(max(0.0, min(1.0, model_probability)) * 100)
    rules_score, reasons = evaluate_rules(features, city)

    score = round(MODEL_WEIGHT * model_score + RULES_WEIGHT * rules_score)
    score = max(0, min(100, score))
    status = status_from_score(score)

    if status != Status.APPROVED and not reasons:
        reasons = [MODEL_ONLY_REASON]

    return RiskResult(
        risk_score=score,
        status=status,
        reasons=reasons,
        model_score=model_score,
        rules_score=rules_score,
    )
