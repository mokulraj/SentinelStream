# app/schemas/transaction.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# ------------------------------
# Request Schema for Creating Transaction
# ------------------------------
class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be greater than 0")
    transaction_type: Optional[str] = Field(default="purchase", description="Type of transaction")
    location: Optional[str] = Field(None, description="Transaction location")
    merchant: Optional[str] = Field(None, description="Merchant name")

# ------------------------------
# Response Schema for Transaction
# ------------------------------
class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    location: Optional[str]
    merchant: Optional[str]
    status: str
    risk_score: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

# ------------------------------
# Response after creating a transaction
# ------------------------------
class TransactionCreateResponse(BaseModel):
    message: str
    transaction: TransactionResponse
