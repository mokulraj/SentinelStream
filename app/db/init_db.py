# create_tables.py
import asyncio
from app.db.session import async_engine
from app.db.base import Base

async def init_models():
    async with async_engine.begin() as conn:
        # This will create all tables (users, transactions)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())
