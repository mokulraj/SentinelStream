# init_transactions.py
import asyncio
from sqlalchemy import text  # <--- IMPORTANT
from app.db.base import Base
from app.db.session import engine

async def init_transactions():
    async with engine.begin() as conn:
        # DROP TABLE using sqlalchemy.text()
        await conn.run_sync(lambda sync_conn: sync_conn.execute(text("DROP TABLE IF EXISTS transactions")))
        # Create all tables according to updated models
        await conn.run_sync(Base.metadata.create_all)
    print("Transactions table recreated successfully!")

if __name__ == "__main__":
    asyncio.run(init_transactions())
