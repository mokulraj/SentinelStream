from fastapi import FastAPI
<<<<<<< HEAD
from app.api.routes_auth import router as auth_router
from app.api.routes_transactions import router as tx_router
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.transaction import Transaction

app = FastAPI(title="SentinelStream")

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
app.include_router(tx_router)

@app.get("/")
def root():
    return {"message": "SentinelStream API Running"}

@app.get("/health")
def health():
    return {"status": "ok"}
=======

app = FastAPI(title="SentinelStream")

@app.get("/")
def root():
    return {"message": "SentinelStream API Running"}
>>>>>>> 9038bf346d05a88bc7b02e1d5d78ba7d2ab126e0
