# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from app.db.session import get_db
# from app.db.models.user import User
# from app.schemas.user import UserRegister, UserLogin, TokenResponse
# from app.core.security import hash_password, verify_password, create_access_token

# router = APIRouter(prefix="/auth", tags=["Auth"])


# # ----------------------------
# # Register Endpoint
# # ----------------------------
# @router.post("/register", status_code=201)
# async def register_user(payload: UserRegister, db: AsyncSession = Depends(get_db)):
#     # Check if user already exists
#     result = await db.execute(select(User).where(User.email == payload.email))
#     user = result.scalars().first()
#     if user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Hash password and create user
#     new_user = User(
#         email=payload.email,
#         hashed_password=hash_password(payload.password)
#     )
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)

#     # Return success message (no token)
#     return {"message": "User registered successfully", "user_id": new_user.id}


# # ----------------------------
# # Login Endpoint
# # ----------------------------
# @router.post("/login", response_model=TokenResponse)
# async def login_user(payload: UserLogin, db: AsyncSession = Depends(get_db)):
#     # Find user by email
#     result = await db.execute(select(User).where(User.email == payload.email))
#     user = result.scalars().first()

#     # Verify user exists and password is correct
#     if not user or not verify_password(payload.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     # Create JWT token
#     token = create_access_token({"sub": user.email})
#     return {"access_token": token, "token_type": "bearer"}

# edited version:--------------------------
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth2 for Swagger Authorize button (uses hidden endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login_form")

# ----------------------------
# Register Endpoint
# ----------------------------
@router.post("/register", status_code=201, summary="Register a new user")
async def register_user(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")

    return {"message": "User registered successfully", "user_id": new_user.id}

# ----------------------------
# Login Endpoint (JSON) - Swagger visible
# ----------------------------
@router.post("/login_json", response_model=TokenResponse, summary="Login User with JSON")
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

# ----------------------------
# Login Endpoint (Form) for Swagger Authorize - Hidden
# ----------------------------
@router.post("/login_form", response_model=TokenResponse, include_in_schema=False)
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

__all__ = ["router", "get_current_user"]
