from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, verify_password
import jwt
from datetime import datetime, timedelta

# JWT config
JWT_SECRET = "supersecretkey"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 1

async def create_user(db: AsyncSession, email: str, password: str):
    user = User(
        email=email,
        password=hash_password(password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)  # fetch the latest user instance
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_jwt_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

async def login_user(db: AsyncSession, email: str, password: str):
    user = await authenticate_user(db, email, password)
    if not user:
        return None
    token = create_jwt_token(user.email)
    # Optional: store token somewhere (database or cache) if needed
    return token
