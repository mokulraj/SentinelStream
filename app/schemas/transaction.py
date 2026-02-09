from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float
    transaction_type: str
    location: str | None = None
    merchant: str | None = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    location: str | None
    merchant: str | None
    status: str
    risk_score: float
    created_at: datetime

    class Config:
        from_attributes = True
