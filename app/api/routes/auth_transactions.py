# app/api/routes/auth_transactions.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from app.db.session import get_db
from app.db.models.user import User
from app.db.models.transaction import Transaction
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# OAuth2 for Swagger Authorize button (hidden endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login_form")

# ----------------------------
# Auth Endpoints
# ----------------------------
@router.post("/auth/register", status_code=201, summary="Register a new user")
async def register_user(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(payload.password)
    new_user = User(email=payload.email, hashed_password=hashed_pw)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")

    return {"message": "User registered successfully", "user_id": new_user.id}


@router.post("/auth/login_json", response_model=TokenResponse, summary="Login User with JSON")
async def login_user_json(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/login_form", response_model=TokenResponse, include_in_schema=False)
async def login_user_form(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer"}


# ----------------------------
# JWT Dependency
# ----------------------------
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


# ----------------------------
# Transactions Endpoints
# ----------------------------
@router.get("/transactions", response_model=list[TransactionResponse])
async def list_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transaction).where(Transaction.user_id == current_user.id))
    transactions = result.scalars().all()
    return transactions


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_tx = Transaction(
        user_id=current_user.id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        location=transaction.location,
        merchant=transaction.merchant,
        status="success",
        risk_score=0.0
    )
    db.add(new_tx)
    await db.commit()
    await db.refresh(new_tx)
    return new_tx


__all__ = ["router", "get_current_user"]
