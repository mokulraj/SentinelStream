from pydantic import BaseModel
from datetime import datetime


class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    currency: str


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
