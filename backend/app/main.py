"""Punto de entrada de la API de FinansChecker

En local: uvicorn app.main:app --reload
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.error_handlers import register_error_handlers
from app.api.routes import router
from app.infrastructure.config import get_settings
from app.infrastructure.ml_model import ModelFileError, SklearnRiskModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("finanschecker")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # El modelo se carga una sola vez al iniciar, si falla la API sigue respondiendo
    # consultas y solo rechaza nuevas evaluaciones con un error 503
    settings = get_settings()
    try:
        app.state.model = SklearnRiskModel.load(settings.model_path)
        logger.info("Modelo de IA cargado desde %s", settings.model_path)
    except (ModelFileError, OSError, ValueError) as exc:
        app.state.model = None
        logger.error("No se pudo cargar el modelo de IA: %s", exc)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="FinansChecker API",
        description="Detección de transacciones sospechosas con IA, todas las transacciones son simuladas",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.state.model = None
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    register_error_handlers(app)
    app.include_router(router)
    return app


app = create_app()
