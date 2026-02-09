from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    currency: str
    type: str  # debit or credit

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
