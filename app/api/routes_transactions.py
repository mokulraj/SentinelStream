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
