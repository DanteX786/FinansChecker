"""Conecta los casos de uso con sus implementaciones concretas"""

from collections.abc import Iterator

import psycopg
from fastapi import Depends, Request

from app.application.use_cases import (
    EvaluateTransaction,
    GetStats,
    GetTransactionDetail,
    ListAlerts,
    ListTransactions,
    ListUsers,
)
from app.infrastructure.database import connect
from app.infrastructure.repositories import (
    PostgresAlertRepository,
    PostgresStatsRepository,
    PostgresTransactionRepository,
    PostgresUserRepository,
)


def get_connection() -> Iterator[psycopg.Connection]:
    with connect() as conn:
        yield conn


def get_evaluate_transaction(request: Request, conn=Depends(get_connection)) -> EvaluateTransaction:
    return EvaluateTransaction(
        users=PostgresUserRepository(conn),
        transactions=PostgresTransactionRepository(conn),
        model=request.app.state.model,
    )


def get_list_transactions(conn=Depends(get_connection)) -> ListTransactions:
    return ListTransactions(PostgresTransactionRepository(conn))


def get_transaction_detail(conn=Depends(get_connection)) -> GetTransactionDetail:
    return GetTransactionDetail(PostgresTransactionRepository(conn))


def get_list_alerts(conn=Depends(get_connection)) -> ListAlerts:
    return ListAlerts(PostgresAlertRepository(conn))


def get_stats(conn=Depends(get_connection)) -> GetStats:
    return GetStats(PostgresStatsRepository(conn))


def get_list_users(conn=Depends(get_connection)) -> ListUsers:
    return ListUsers(PostgresUserRepository(conn))
