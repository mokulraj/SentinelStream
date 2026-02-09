<<<<<<< HEAD
# app/models/user.py
=======
>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
<<<<<<< HEAD
    __table_args__ = {'extend_existing': True}  # prevents table already defined error
=======
>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
