# app/services/transaction_service.py

import uuid
import time
import asyncio
from datetime import datetime
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.ml.fraud_model import get_risk_score
from app.worker.celery_app import send_alert_email

import logging

logger = logging.getLogger(__name__)

# Async wrapper for ML scoring
async def get_risk_score_async(amount: float, txn_count_today: int) -> float:
    return await asyncio.to_thread(get_risk_score, amount, txn_count_today)


async def evaluate_risk(transaction: TransactionCreate, current_user, db: AsyncSession) -> dict:
    """Evaluate risk for a transaction."""
    today = datetime.utcnow().date()
    txn_count_query = await db.execute(
        select(func.count(Transaction.id)).where(
            Transaction.user_id == current_user.id,
            func.date(Transaction.created_at) == today
        )
    )
    txn_count_today = txn_count_query.scalar() or 0

    risk_score = await get_risk_score_async(transaction.amount, txn_count_today)

    status = "approved"
    reason = None

    if transaction.amount > 10000:
        risk_score = max(risk_score, 0.95)
        status = "declined"
        reason = "Amount exceeds limit"
    elif transaction.amount > 5000:
        risk_score = max(risk_score, 0.6)
        status = "approved"
        reason = "High-value transaction, manual review recommended"

    if transaction.merchant and "suspicious" in transaction.merchant.lower():
        risk_score = max(risk_score, 0.9)
        status = "declined"
        reason = "Suspicious merchant detected"

    logger.info(f"Risk evaluated for user {current_user.id}: score={risk_score}, status={status}")
    return {"status": status, "risk_score": risk_score, "reason": reason}


async def create_transaction(db: AsyncSession, current_user, payload: TransactionCreate) -> Transaction:
    """Create transaction and trigger alerts if necessary."""
    start_time = time.time()
    risk_result = await evaluate_risk(payload, current_user, db)

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

    setattr(new_tx, "transaction_uuid", transaction_uuid)
    setattr(new_tx, "decline_reason", risk_result.get("reason"))
    setattr(new_tx, "execution_time", 0)

    db.add(new_tx)
    try:
        await db.commit()
        await db.refresh(new_tx)
    except Exception as e:
        await db.rollback()
        logger.error(f"DB commit failed for transaction {transaction_uuid}: {e}")
        raise

    new_tx.execution_time = round(time.time() - start_time, 4)

    # Send email
    use_mailhog = os.environ.get("EMAIL_DEV", "True").lower() in ["true", "1", "yes"]

    if new_tx.risk_score >= 0.7:
        if use_mailhog:
            send_alert_email.apply(
                args=(current_user.email, new_tx.id, new_tx.risk_score),
                kwargs={
                    "amount": new_tx.amount,
                    "merchant": new_tx.merchant,
                    "transaction_uuid": new_tx.transaction_uuid
                }
            )
            logger.info(f"[DEV] Alert email sent immediately for transaction {new_tx.id}")
        else:
            send_alert_email.delay(
                to_email=current_user.email,
                txn_id=new_tx.id,
                risk_score=new_tx.risk_score,
                amount=new_tx.amount,
                merchant=new_tx.merchant,
                transaction_uuid=transaction_uuid,
            )
            logger.info(f"[PROD] Alert email enqueued for transaction {new_tx.id}")

    return new_tx


async def list_user_transactions(db: AsyncSession, current_user, skip=0, limit=10):
    """List user's transactions."""
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    transactions = result.scalars().all()

    for tx in transactions:
        if not hasattr(tx, "transaction_uuid"):
            setattr(tx, "transaction_uuid", str(uuid.uuid4()))
        if not hasattr(tx, "execution_time"):
            setattr(tx, "execution_time", 0)
        if not hasattr(tx, "decline_reason"):
            setattr(tx, "decline_reason", None)

    return transactions