from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer
from typing import List

from app.db.session import get_db
from app.db.models.fraud_rule import FraudRule
from app.schemas.transaction import TransactionCreate, TransactionOut
from app.core.rules_engine import evaluate_transaction
from app.routes.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/", response_model=TransactionOut)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # Optional: decode token to get user id if needed
    current_user = await get_current_user(token, db)

    # Fetch all active rules
    result = await db.execute(select(FraudRule).where(FraudRule.enabled==True))
    rules: List[FraudRule] = result.scalars().all()

    # Add user home location for demo (replace with real DB lookup)
    transaction_dict = transaction.dict()
    transaction_dict["user_home_location"] = "delhi"

    # Evaluate rules
    triggered_rules = evaluate_transaction(transaction_dict, rules)

    # Determine decision
    if triggered_rules:
        decision = "DECLINE"
    else:
        decision = "APPROVE"

    return {
        **transaction_dict,
        "rules_triggered": triggered_rules,
        "decision": decision
    }
