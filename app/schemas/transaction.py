from pydantic import BaseModel

class TransactionCreate(BaseModel):
    amount: float
    type: str   # debit or credit

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    status: str


