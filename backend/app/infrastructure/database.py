from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from app.infrastructure.config import get_settings


class DatabaseNotConfiguredError(Exception):
    """Falta la variable DATABASE_URL"""


@contextmanager
def connect(database_url: str | None = None) -> Iterator[psycopg.Connection]:
    """Abre una conexión a PostgreSQL y la cierra al terminar

    Neon exige SSL, por eso la cadena de conexión debe incluir sslmode=require
    """
    url = database_url or get_settings().database_url
    if not url:
        raise DatabaseNotConfiguredError()
    with psycopg.connect(url, row_factory=dict_row, connect_timeout=10) as conn:
        yield conn
