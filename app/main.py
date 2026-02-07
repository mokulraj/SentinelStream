from fastapi import FastAPI
import uvicorn

from app.api.routes.auth import router as auth_router
from app.api.routes_transactions import router as tx_router
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="SentinelStream")


@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ✅ Routers
app.include_router(auth_router)        # /auth/*
app.include_router(tx_router)          # /transactions/* (or whatever prefix inside)


@app.get("/")
def root():
    return {"message": "SentinelStream API Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
