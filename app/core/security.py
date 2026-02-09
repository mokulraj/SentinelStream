# # app/core/security.py
# from datetime import datetime, timedelta
# from jose import jwt
# from passlib.context import CryptContext

# # --------------------------
# # JWT / Password Config
# # --------------------------
# SECRET_KEY = "SENTINELSTREAM_SECRET_KEY"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Using bcrypt for password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# BCRYPT_MAX_LENGTH = 72  # bcrypt max password length in bytes

# # --------------------------
# # Password hashing
# # --------------------------
# def hash_password(password: str) -> str:
#     """
#     Safely hash password for bcrypt, truncating at 72 bytes.
#     """
#     password_bytes = password.encode("utf-8")[:BCRYPT_MAX_LENGTH]  # truncate safely
#     return pwd_context.hash(password_bytes)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Safely verify password, truncating to 72 bytes.
#     """
#     password_bytes = plain_password.encode("utf-8")[:BCRYPT_MAX_LENGTH]  # truncate safely
#     return pwd_context.verify(password_bytes, hashed_password)


# # --------------------------
# # JWT token creation
# # --------------------------
# def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# edited version:--------------------------

# app/core/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

# --------------------------
# JWT / Password Config
# --------------------------
SECRET_KEY = "SENTINELSTREAM_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Using bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BCRYPT_MAX_LENGTH = 72  # bcrypt max password length in bytes

# --------------------------
# Password hashing
# --------------------------
def hash_password(password: str) -> str:
    """
    Safely hash password for bcrypt, truncating at 72 bytes.
    """
    password_bytes = password.encode("utf-8")[:BCRYPT_MAX_LENGTH]  # truncate safely
    return pwd_context.hash(password_bytes)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Safely verify password, truncating to 72 bytes.
    """
    password_bytes = plain_password.encode("utf-8")[:BCRYPT_MAX_LENGTH]  # truncate safely
    return pwd_context.verify(password_bytes, hashed_password)


# --------------------------
# JWT token creation
# --------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token with optional expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --------------------------
# JWT token decoding
# --------------------------
def decode_access_token(token: str) -> dict:
    """
    Decode JWT token and return payload.
    Raises JWTError if invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise e
