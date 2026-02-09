<<<<<<< HEAD
# app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from app.db.session import get_db
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
=======
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13

router = APIRouter(prefix="/auth", tags=["Auth"])


<<<<<<< HEAD
@router.post("/register", status_code=201)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    Uses safe password hashing compatible with bcrypt's 72-byte limit.
    """
    from app.models.user import User  # avoid circular import

    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password safely (handles long passwords)
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
=======
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13
    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
<<<<<<< HEAD
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    Uses safe password verification compatible with bcrypt's 72-byte limit.
    """
    from app.models.user import User

    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()

    # Verify credentials
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}
=======
async def login_user(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token({"user_id": user.id})

    return TokenResponse(access_token=access_token)
>>>>>>> 6cc52ffcbaf4b67a21040345c8d5e46f7ffcdf13
