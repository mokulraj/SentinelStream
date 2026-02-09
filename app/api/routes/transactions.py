from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse

from app.fraud.rule_engine import rule_based_fraud
from app.fraud.ml_engine import ml_risk_score
from app.fraud.decision_engine import final_decision

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    payload: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    user_home_location = "India"  # mocked profile (Redis later)

    rule_result = rule_based_fraud(
        payload.amount,
        payload.location,
        user_home_location
    )

    ml_score = ml_risk_score(payload.amount)
    status = final_decision(rule_result, ml_score)

    txn = Transaction(
        user_id=user_id,
        amount=payload.amount,
        location=payload.location,
        merchant=payload.merchant,
        risk_score=ml_score,
        status=status
    )

    db.add(txn)
    await db.commit()
    await db.refresh(txn)

    return txn
