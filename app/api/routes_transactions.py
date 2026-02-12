from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import redis
import time

from app.api.deps import get_db, get_current_user
from app.schemas.transaction import TransactionCreate
from app.services.rules_engine import apply_rules
from app.services.ml_engine import ml_risk_score
from app.services.transaction_service import create_transaction, get_balance
from app.core.config import REDIS_URL

router = APIRouter(prefix="/transactions", tags=["Transactions"])

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_financial_transaction(
    data: TransactionCreate,
    idempotency_key: str = Header(...),
    db: AsyncSession = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    start_time = time.perf_counter()

    # 1️⃣ Idempotency check (Bank-grade safety)
    if redis_client.get(idempotency_key):
        return {
            "status": "DUPLICATE",
            "message": "Duplicate transaction request ignored"
        }

    # 2️⃣ Balance validation
    balance = await get_balance(db, user_email)

    if data.type == "debit" and balance < data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )

    # 3️⃣ Fraud detection
    rules_triggered = apply_rules(data)
    ml_score = ml_risk_score(data)

    if "HIGH_AMOUNT" in rules_triggered or ml_score > 0.9:
        decision = "DECLINED"
        risk_level = "CRITICAL"
    elif ml_score > 0.7:
        decision = "FLAGGED"
        risk_level = "MEDIUM"
    else:
        decision = "APPROVED"
        risk_level = "LOW"

    # 4️⃣ Persist transaction
    transaction = await create_transaction(
        db=db,
        user_email=user_email,
        amount=data.amount,
        tx_type=data.type,
        decision=decision,
        risk_score=ml_score
    )

    # 5️⃣ Store idempotency key
    redis_client.set(idempotency_key, transaction.id, ex=60)

    execution_time = round((time.perf_counter() - start_time) * 1000, 2)

    # 6️⃣ Rich response (THIS is what impresses)
    return {
        "transaction_id": transaction.id,
        "decision": decision,
        "risk_level": risk_level,
        "rules_triggered": rules_triggered,
        "ml_risk_score": round(ml_score, 2),
        "processing_time_ms": execution_time,
        "status": "SUCCESS"
    }