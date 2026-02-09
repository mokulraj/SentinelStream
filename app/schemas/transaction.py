from pydantic import BaseModel
<<<<<<< HEAD
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
=======

class TransactionCreate(BaseModel):
    amount: float
    type: str   # debit or credit

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    status: str


>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13
