from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# --------------------------
# Database URL
# --------------------------
DATABASE_URL = "sqlite+aiosqlite:///./sentinelstream.db"

# --------------------------
# Async Engine
# --------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

# --------------------------
# Async Session
# --------------------------
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# --------------------------
# Dependency for FastAPI
# --------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
