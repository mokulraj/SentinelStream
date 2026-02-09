# app/core/security.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "SENTINELSTREAM_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BCRYPT_MAX_LENGTH = 72


def hash_password(password: str) -> str:
    """
    Safely hash password for bcrypt, truncating at 72 bytes.
    """
    truncated = password.encode("utf-8")[:BCRYPT_MAX_LENGTH].decode("utf-8", "ignore")
    return pwd_context.hash(truncated)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Safely verify password, truncating to 72 bytes.
    """
    truncated = plain_password.encode("utf-8")[:BCRYPT_MAX_LENGTH].decode("utf-8", "ignore")
    return pwd_context.verify(truncated, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
