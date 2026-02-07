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
