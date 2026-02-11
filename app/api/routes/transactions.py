from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.api.deps import get_current_user
from app.services.transaction_service import create_transaction, list_user_transactions

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# 🔹 GET /transactions
@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List transactions for the current user (paginated).
    Includes detailed metadata like UUID, decline reason, and execution time.
    """
    try:
        transactions = await list_user_transactions(db, current_user, skip, limit)
        return transactions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch transactions: {str(e)}"
        )


# 🔹 POST /transactions
@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def post_transaction(
    payload: TransactionCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new transaction for the current user.
    Automatically evaluates risk, assigns a unique UUID, calculates execution time,
    and stores reason for declined transactions if any.
    """
    try:
        tx = await create_transaction(db, current_user, payload)
        return tx
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create transaction: {str(e)}"
        )
