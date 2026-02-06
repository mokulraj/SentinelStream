from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import create_transaction
from app.db.session import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/")
async def make_transaction(
    tx: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
    idempotency_key: str = Header(None)
):
    transaction = await create_transaction(db, tx)

    return {
        "id": transaction.id,
        "amount": transaction.amount,
        "type": transaction.type,
        "status": transaction.status
    }
