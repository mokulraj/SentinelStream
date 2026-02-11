from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import asyncio
import json
import datetime

from app.db.session import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import create_transaction, list_user_transactions
from app.api.deps import get_current_user, get_current_user_from_token  # Updated for SSE

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# ------------------------------
# Helper: generate visual fingerprint
# ------------------------------
def generate_visual_fingerprint(tx):
    """
    Creates a simple emoji-based fingerprint:
    - Risk: low🟢, medium🟡, high🔴
    - Amount: small💵, medium💰, large💸
    - Type: deposit⬆️, withdrawal⬇️
    """
    risk = "🟢" if tx.risk_score < 30 else "🟡" if tx.risk_score < 70 else "🔴"
    amount = "💵" if tx.amount < 1000 else "💰" if tx.amount < 10000 else "💸"
    t_type = "⬆️" if tx.transaction_type.lower() == "deposit" else "⬇️"
    return f"{risk}{amount}{t_type}"


# ------------------------------
# GET /transactions
# ------------------------------
@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List transactions for the current user (paginated).
    Includes detailed metadata and visual fingerprint.
    """
    try:
        transactions = await list_user_transactions(db, current_user, skip, limit)
        for tx in transactions:
            tx.visual_fingerprint = generate_visual_fingerprint(tx)
        return transactions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch transactions: {str(e)}"
        )


# ------------------------------
# POST /transactions
# ------------------------------
@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def post_transaction(
    payload: TransactionCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new transaction for the current user.
    Evaluates risk, assigns UUID, calculates execution time,
    stores decline reason if any, and adds a visual fingerprint.
    """
    try:
        tx = await create_transaction(db, current_user, payload)
        tx.visual_fingerprint = generate_visual_fingerprint(tx)
        return tx
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create transaction: {str(e)}"
        )


# ------------------------------
# SSE /transactions/stream
# ------------------------------
@router.get("/stream")
async def stream_transactions(
    current_user=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Stream new transactions in real-time as Server-Sent Events (SSE)
    with JWT token passed via query parameter (?token=...)
    """
    async def event_generator():
        last_seen_id = 0
        while True:
            transactions = await list_user_transactions(db, current_user, skip=0, limit=10)
            new_transactions = [tx for tx in transactions if tx.id > last_seen_id]
            for tx in reversed(new_transactions):
                tx.visual_fingerprint = generate_visual_fingerprint(tx)
                data = {
                    "id": tx.id,
                    "amount": tx.amount,
                    "type": tx.transaction_type,
                    "merchant": tx.merchant,
                    "location": tx.location,
                    "risk_score": tx.risk_score,
                    "status": tx.status,
                    "visual_fingerprint": tx.visual_fingerprint,
                    "created_at": str(tx.created_at)
                }
                yield f"data: {json.dumps(data)}\n\n"
                last_seen_id = max(last_seen_id, tx.id)
            await asyncio.sleep(2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
