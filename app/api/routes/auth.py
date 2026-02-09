from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# ----------------------------
# Register Endpoint
# ----------------------------
@router.post("/register", status_code=201)
async def register_user(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and create user
    new_user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Return success message (no token)
    return {"message": "User registered successfully", "user_id": new_user.id}


# ----------------------------
# Login Endpoint
# ----------------------------
@router.post("/login", response_model=TokenResponse)
async def login_user(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    # Find user by email
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalars().first()

    # Verify user exists and password is correct
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create JWT token
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
