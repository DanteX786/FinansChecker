from pathlib import Path

import joblib

from app.domain.features import FEATURE_NAMES


class ModelFileError(Exception):
    """El archivo del modelo no existe o no corresponde a las variables actuales"""


class SklearnRiskModel:
    """Adaptador del Random Forest entrenado con scikit-learn"""

    def __init__(self, bundle: dict):
        if bundle.get("feature_names") != FEATURE_NAMES:
            raise ModelFileError("El modelo fue entrenado con otras variables, vuelve a ejecutar train_model.py")
        self._model = bundle["model"]
        self.metrics: dict = bundle.get("metrics", {})
        # Índice de la clase "fraude" dentro de las probabilidades del modelo
        self._fraud_index = list(self._model.classes_).index(1)

    @classmethod
    def load(cls, path: Path) -> "SklearnRiskModel":
        if not path.exists():
            raise ModelFileError(f"No existe el modelo en {path}, ejecuta scripts/train_model.py")
        return cls(joblib.load(path))

    def predict_probability(self, features: list[float]) -> float:
        return float(self._model.predict_proba([features])[0][self._fraud_index])
