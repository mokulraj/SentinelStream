from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Auth"])


# -----------------------------
# Register (JSON)
# -----------------------------
@router.post("/register", status_code=201)
async def register_user(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    # Check if email exists
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = hash_password(payload.password)
    if isinstance(hashed_pw, bytes):
        hashed_pw = hashed_pw.decode()

    # Create user
    user = User(email=payload.email, hashed_password=hashed_pw)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # ✅ Return success message instead of token
    return {"message": "User registered successfully"}


# -----------------------------
# Login (JSON ONLY)
# -----------------------------
@router.post("/login", response_model=TokenResponse)
async def login_user(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(
        data={"user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": token, "token_type": "bearer"}
