# create_tables.py
import asyncio
from app.db.session import engine
from app.db.base import Base

async def init_db():
    async with engine.begin() as conn:
        # Create all tables from your models
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
