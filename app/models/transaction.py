from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)         # e.g., "purchase", "transfer"
    location = Column(String, nullable=True)
    merchant = Column(String, nullable=True)
    risk_score = Column(Float, nullable=True)     # for fraud detection
    status = Column(String, nullable=False, default="success")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
