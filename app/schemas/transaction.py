from pydantic import BaseModel
from datetime import datetime

# 🔹 Schema for creating a transaction
class TransactionCreate(BaseModel):
    amount: float
    transaction_type: str
    location: str | None = None
    merchant: str | None = None


# 🔹 Schema for returning transaction details
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

    # ✅ New fields for detailed transaction tracking
    transaction_uuid: str | None = None       # Unique transaction ID
    decline_reason: str | None = None         # Reason for declined transactions
    execution_time: float | None = None       # Time taken to process transaction (in seconds)

    class Config:
        from_attributes = True
