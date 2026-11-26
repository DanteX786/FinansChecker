import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]

# En local las variables vienen del archivo .env, en Render del panel del servicio
load_dotenv(BACKEND_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: list[str]
    model_path: Path


def get_settings() -> Settings:
    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    return Settings(
        database_url=os.getenv("DATABASE_URL", ""),
        cors_origins=[o.strip().rstrip("/") for o in origins.split(",") if o.strip()],
        model_path=Path(os.getenv("MODEL_PATH", str(BACKEND_DIR / "ml" / "model.joblib"))),
    )
