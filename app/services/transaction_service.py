import uuid
import time
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.db.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

# Simulated Risk Engine
async def evaluate_risk(transaction: TransactionCreate) -> dict:
    """
    Evaluate transaction risk and decide if approved or declined.
    Returns a dict with status, risk_score, and reason.
    """
    risk_score = 0.0
    reason = None
    status = "approved"

    # Example rules (can be extended)
    if transaction.amount > 10000:
        risk_score += 90
        status = "declined"
        reason = "Amount exceeds limit"
    elif transaction.amount > 5000:
        risk_score += 50
        status = "approved"
        reason = "High-value transaction, manual review recommended"
    else:
        risk_score += 10

    # Randomly simulate suspicious activity
    # In real project, replace with real fraud detection logic
    if transaction.merchant and "suspicious" in transaction.merchant.lower():
        risk_score += 80
        status = "declined"
        reason = "Suspicious merchant detected"

    return {"status": status, "risk_score": risk_score, "reason": reason}


# Core transaction creation logic
async def create_transaction(
    db: AsyncSession, current_user, payload: TransactionCreate
) -> Transaction:
    start_time = time.time()  # track execution start

    # Evaluate risk
    risk_result = await evaluate_risk(payload)

    # Create unique transaction UUID
    transaction_uuid = str(uuid.uuid4())

    new_tx = Transaction(
        user_id=current_user.id,
        amount=payload.amount,
        transaction_type=payload.transaction_type,
        location=payload.location,
        merchant=payload.merchant,
        status=risk_result["status"],
        risk_score=risk_result["risk_score"],
    )

    # Attach UUID to metadata (you can add a new column if needed)
    setattr(new_tx, "transaction_uuid", transaction_uuid)
    setattr(new_tx, "decline_reason", risk_result.get("reason"))
    setattr(new_tx, "execution_time", 0)  # temporary placeholder

    db.add(new_tx)

    try:
        await db.commit()
        await db.refresh(new_tx)
    except Exception:
        await db.rollback()
        raise

    # Calculate execution time
    end_time = time.time()
    new_tx.execution_time = round(end_time - start_time, 4)

    return new_tx


# List transactions with extra metadata
async def list_user_transactions(db: AsyncSession, current_user, skip=0, limit=10):
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    transactions = result.scalars().all()

    # Attach extra metadata to each transaction
    for tx in transactions:
        if not hasattr(tx, "transaction_uuid"):
            setattr(tx, "transaction_uuid", str(uuid.uuid4()))
        if not hasattr(tx, "execution_time"):
            setattr(tx, "execution_time", 0)
        if not hasattr(tx, "decline_reason"):
            setattr(tx, "decline_reason", None)

    return transactions
