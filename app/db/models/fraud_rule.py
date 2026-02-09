from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.base import Base

class FraudRule(Base):
    __tablename__ = "fraud_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)            # e.g., "High Amount"
    rule_type = Column(String, nullable=False)       # e.g., "AMOUNT_LIMIT"
    threshold = Column(Float, nullable=True)         # e.g., 5000
    enabled = Column(Boolean, default=True)
