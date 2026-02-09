<<<<<<< HEAD
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.schemas.transaction import TransactionCreate
from app.services.rules_engine import apply_rules
from app.services.ml_engine import ml_risk_score

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    rules_hit = apply_rules(data)
    ml_score = ml_risk_score(data)

    if "HIGH_AMOUNT" in rules_hit:
        decision = "DECLINE"
    elif ml_score > 0.7:
        decision = "FLAG"
    else:
        decision = "APPROVE"

    # TODO: save transaction + decision to DB (real insert)

    return {
        "decision": decision,
        "rules_triggered": rules_hit,
        "ml_score": round(ml_score, 2)
    }
=======
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import redis
from app.api.deps import get_db, get_current_user
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import create_transaction, get_balance
from app.core.config import REDIS_URL

router = APIRouter(prefix="/transactions")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

@router.post("/")
async def make_transaction(
    data: TransactionCreate,
    idempotency_key: str = Header(...),
    db: AsyncSession = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    if r.get(idempotency_key):
        return {"message": "Duplicate request"}

    balance = await get_balance(db, 1)

    if data.type == "debit" and balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    tx = await create_transaction(db, 1, data.amount, data.type, user_email)

    r.set(idempotency_key, "done", ex=60)

    return tx
>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13
