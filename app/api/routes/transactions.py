# app/api/routes/transactions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.db.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.api.routes.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# ----------------------------
# List all transactions for current user
# ----------------------------
@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transaction).where(Transaction.user_id == current_user.id))
    transactions = result.scalars().all()
    return transactions

# ----------------------------
# Create a transaction
# ----------------------------
@router.post("/", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    payload: TransactionCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # ⚠️ IMPORTANT: your model uses 'type', but Pydantic should match it safely
    # We'll remove 'type' from TransactionCreate to avoid SQLAlchemy keyword conflict

    new_tx = Transaction(
        user_id=current_user.id,
        amount=payload.amount,
        location=payload.location,
        status="success",
        risk_score=0.0  # default, you can integrate your fraud scoring later
    )

    db.add(new_tx)
    try:
        await db.commit()
        await db.refresh(new_tx)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")

    return new_tx
