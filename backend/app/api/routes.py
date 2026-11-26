"""Rutas de la API, solo reciben, delegan en los casos de uso y responden"""

from fastapi import APIRouter, Depends, Query, Request

from app.api import dependencies as deps
from app.api.schemas import (
    AlertOut,
    EvaluationOut,
    HealthOut,
    StatsOut,
    TransactionCreate,
    TransactionDetailOut,
    TransactionOut,
    UserOut,
)
from app.application.use_cases import (
    EvaluateTransaction,
    GetStats,
    GetTransactionDetail,
    ListAlerts,
    ListTransactions,
    ListUsers,
)
from app.domain.entities import NewTransaction, Status, now_colombia

router = APIRouter()


@router.get("/health", response_model=HealthOut, tags=["Sistema"])
def health(request: Request) -> HealthOut:
    return HealthOut(status="ok", model_loaded=request.app.state.model is not None)


@router.get("/users", response_model=list[UserOut], tags=["Usuarios"])
def list_users(use_case: ListUsers = Depends(deps.get_list_users)) -> list[UserOut]:
    return [UserOut.from_domain(u) for u in use_case.execute()]


@router.post("/transactions", response_model=EvaluationOut, status_code=201, tags=["Transacciones"])
def create_transaction(
    payload: TransactionCreate,
    use_case: EvaluateTransaction = Depends(deps.get_evaluate_transaction),
) -> EvaluationOut:
    tx = NewTransaction(
        user_id=payload.user_id,
        type=payload.type,
        amount=payload.amount,
        destination_account=payload.destination_account,
        city=payload.city,
        channel=payload.channel,
        created_at=payload.created_at or now_colombia(),
    )
    outcome = use_case.execute(tx)
    return EvaluationOut(
        transaction=TransactionOut.from_domain(outcome.transaction),
        reasons=outcome.result.reasons,
        alert_created=outcome.result.needs_alert,
    )


@router.get("/transactions", response_model=list[TransactionOut], tags=["Transacciones"])
def list_transactions(
    status: Status | None = None,
    limit: int = Query(default=200, ge=1, le=500),
    use_case: ListTransactions = Depends(deps.get_list_transactions),
) -> list[TransactionOut]:
    return [TransactionOut.from_domain(t) for t in use_case.execute(status, limit)]


@router.get("/transactions/{transaction_id}", response_model=TransactionDetailOut, tags=["Transacciones"])
def get_transaction(
    transaction_id: int,
    use_case: GetTransactionDetail = Depends(deps.get_transaction_detail),
) -> TransactionDetailOut:
    return TransactionDetailOut.from_domain(use_case.execute(transaction_id))


@router.get("/alerts", response_model=list[AlertOut], tags=["Alertas"])
def list_alerts(
    limit: int = Query(default=100, ge=1, le=500),
    use_case: ListAlerts = Depends(deps.get_list_alerts),
) -> list[AlertOut]:
    return [AlertOut.from_domain(a) for a in use_case.execute(limit)]


@router.get("/stats", response_model=StatsOut, tags=["Dashboard"])
def get_stats(
    days: int = Query(default=14, ge=1, le=90),
    use_case: GetStats = Depends(deps.get_stats),
) -> StatsOut:
    return StatsOut.from_domain(use_case.execute(days))
