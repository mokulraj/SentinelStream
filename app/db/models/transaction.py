# app/db/models/transaction.py
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False, default="purchase")  # renamed to match schema
    location = Column(String, nullable=True)
    merchant = Column(String, nullable=True)
    risk_score = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="success")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to User
    user = relationship("User", back_populates="transactions")
