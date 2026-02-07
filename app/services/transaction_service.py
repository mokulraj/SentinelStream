from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.transaction import Transaction
from app.services.fraud_service import check_fraud
from app.workers.tasks import send_fraud_alert
from app.core.token_manager import get_token
import requests

def get_transactions():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://127.0.0.1:8000/protected-route", headers=headers)
    return response.json()



async def get_balance(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(func.sum(Transaction.amount))
        .where(Transaction.user_id == user_id)
    )
    return result.scalar() or 0

async def create_transaction(db: AsyncSession, user_id: int, amount: float, t_type: str, email: str):
    if t_type == "debit":
        amount = -abs(amount)

    is_fraud = check_fraud(abs(amount))

    status = "fraud" if is_fraud else "success"

    tx = Transaction(
        user_id=user_id,
        amount=amount,
        type=t_type,
        status=status
    )

    db.add(tx)
    await db.commit()
    await db.refresh(tx)

    if is_fraud:
        send_fraud_alert.delay(email, abs(amount))

    return tx
