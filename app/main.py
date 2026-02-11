from fastapi import FastAPI, Query, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.api.routes.auth import router as auth_router
from app.api.routes.transactions import router as tx_router
from app.db.session import engine
from app.db.base import Base
from app.db import models  # ensures models are registered
from app.api.deps import get_current_user_from_token  # New helper to get user from query param

# ------------------------------
# Lifespan
# ------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


# ------------------------------
# App Instance
# ------------------------------
app = FastAPI(
    title="SentinelStream",
    lifespan=lifespan,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": False
    }
)

# ------------------------------
# Mount Static Folder for Dashboard
# ------------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ------------------------------
# Routers
# ------------------------------
app.include_router(auth_router)
app.include_router(tx_router)

# ------------------------------
# Root and Health
# ------------------------------
@app.get("/")
async def root():
    return {"message": "SentinelStream API Running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# ------------------------------
# Run
# ------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
