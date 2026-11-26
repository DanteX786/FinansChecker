"""Entrena el Random Forest de FinansChecker y lo guarda en ml/model.joblib

Uso, desde la carpeta backend:
    python -m scripts.train_model
"""

from collections import defaultdict
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split

from app.domain.entities import PastTransaction, Status
from app.domain.features import FEATURE_NAMES, build_features
from app.domain.risk_rules import combine
from scripts.data_generator import generate_dataset

MODEL_PATH = Path(__file__).resolve().parents[1] / "ml" / "model.joblib"


def build_training_set():
    """Calcula las variables de cada transacción con el historial que tenía en ese momento"""
    users, transactions = generate_dataset()
    user_city = {u.id: u.city for u in users}
    history: dict[int, list[PastTransaction]] = defaultdict(list)
    rows, labels, cities = [], [], []

    for tx in transactions:
        features = build_features(
            amount=tx.amount,
            tx_type=tx.type,
            channel=tx.channel,
            city=tx.city,
            destination_account=tx.destination_account,
            created_at=tx.created_at,
            user_city=user_city[tx.user_id],
            history=history[tx.user_id],
        )
        rows.append(features)
        labels.append(1 if tx.is_fraud else 0)
        cities.append(tx.city)
        history[tx.user_id].append(PastTransaction(tx.amount, tx.destination_account, tx.created_at))

    return rows, labels, cities


def main() -> None:
    features, labels, cities = build_training_set()
    vectors = [f.to_vector() for f in features]
    indices = list(range(len(vectors)))

    train_idx, test_idx = train_test_split(indices, test_size=0.25, stratify=labels, random_state=42)

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
    )
    model.fit([vectors[i] for i in train_idx], [labels[i] for i in train_idx])

    y_test = [labels[i] for i in test_idx]
    y_model = model.predict([vectors[i] for i in test_idx])

    # También se mide el resultado final que ve el usuario, modelo y reglas combinados
    fraud_index = list(model.classes_).index(1)
    probabilities = model.predict_proba([vectors[i] for i in test_idx])[:, fraud_index]
    y_combined = [
        1 if combine(p, features[i], cities[i]).status != Status.APPROVED else 0
        for p, i in zip(probabilities, test_idx)
    ]

    metrics = {
        "samples": len(vectors),
        "fraud_samples": sum(labels),
        "model_precision": round(precision_score(y_test, y_model), 3),
        "model_recall": round(recall_score(y_test, y_model), 3),
        "combined_precision": round(precision_score(y_test, y_combined), 3),
        "combined_recall": round(recall_score(y_test, y_combined), 3),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_names": FEATURE_NAMES, "metrics": metrics}, MODEL_PATH, compress=3)

    print("Modelo entrenado y guardado en", MODEL_PATH)
    print(f"Transacciones: {metrics['samples']} (fraudes simulados: {metrics['fraud_samples']})")
    print(f"Modelo de IA       precisión {metrics['model_precision']:.1%}  recall {metrics['model_recall']:.1%}")
    print(f"Modelo + reglas    precisión {metrics['combined_precision']:.1%}  recall {metrics['combined_recall']:.1%}")


if __name__ == "__main__":
    main()
