from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

async def create_transaction(db: AsyncSession, tx: TransactionCreate):
    new_tx = Transaction(
        amount=tx.amount,
        type=tx.type,
        status="success"
    )
    db.add(new_tx)
    await db.commit()
    await db.refresh(new_tx)
    return new_tx
