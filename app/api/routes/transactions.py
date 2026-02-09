from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.db.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.api.deps import get_current_user   # ✅ CORRECT PLACE

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# 🔹 GET /transactions (paginated, user-scoped)
@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


# 🔹 POST /transactions
@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: TransactionCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_tx = Transaction(
        user_id=current_user.id,   # 🔐 critical
        amount=payload.amount,
        transaction_type=payload.transaction_type,
        location=payload.location,
        merchant=payload.merchant,
        status="success",
        risk_score=0.0
    )

    db.add(new_tx)

    try:
        await db.commit()
        await db.refresh(new_tx)
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create transaction"
        )

    return new_tx
