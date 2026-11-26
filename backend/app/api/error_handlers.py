"""Convierte los errores en respuestas claras, sin mostrar detalles internos"""

import logging

import psycopg
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.schemas import FIELD_MESSAGES
from app.application.errors import ModelNotAvailableError, TransactionNotFoundError, UserNotFoundError
from app.infrastructure.database import DatabaseNotConfiguredError

logger = logging.getLogger("finanschecker")


def _error(status_code: int, message: str, errors: dict[str, str] | None = None) -> JSONResponse:
    body: dict = {"message": message}
    if errors:
        body["errors"] = errors
    return JSONResponse(status_code=status_code, content=body)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_error(_: Request, exc: RequestValidationError):
        errors: dict[str, str] = {}
        for err in exc.errors():
            loc = [str(part) for part in err.get("loc", []) if part != "body"]
            field = loc[0] if loc else "general"
            errors.setdefault(field, FIELD_MESSAGES.get(field, "Dato inválido"))
        return _error(422, "Hay datos inválidos, revisa los campos marcados", errors)

    @app.exception_handler(UserNotFoundError)
    async def user_not_found(_: Request, __: UserNotFoundError):
        return _error(404, "El usuario seleccionado no existe", {"user_id": "El usuario seleccionado no existe"})

    @app.exception_handler(TransactionNotFoundError)
    async def transaction_not_found(_: Request, __: TransactionNotFoundError):
        return _error(404, "La transacción no existe")

    @app.exception_handler(ModelNotAvailableError)
    async def model_not_available(_: Request, __: ModelNotAvailableError):
        logger.error("Se intentó evaluar una transacción sin el modelo de IA cargado")
        return _error(503, "El motor de riesgo no está disponible en este momento, intenta más tarde")

    @app.exception_handler(DatabaseNotConfiguredError)
    async def database_not_configured(_: Request, __: DatabaseNotConfiguredError):
        logger.error("Falta la variable de entorno DATABASE_URL")
        return _error(503, "No pudimos conectar con la base de datos, intenta de nuevo")

    @app.exception_handler(psycopg.OperationalError)
    async def database_unavailable(_: Request, exc: psycopg.OperationalError):
        logger.error("Error de conexión con la base de datos: %s", exc)
        return _error(503, "No pudimos conectar con la base de datos, intenta de nuevo")

    @app.exception_handler(Exception)
    async def unexpected_error(_: Request, exc: Exception):
        logger.exception("Error inesperado", exc_info=exc)
        return _error(500, "No pudimos procesar la solicitud, intenta de nuevo")
