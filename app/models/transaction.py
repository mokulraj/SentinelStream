<<<<<<< HEAD
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


=======
from sqlalchemy import Column, Integer, Float, String
from app.db.base import Base

>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    amount = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    merchant = Column(String, nullable=False)

    risk_score = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
=======
    amount = Column(Float)
    type = Column(String)
    status = Column(String, default="success")
>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13
