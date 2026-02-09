# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# from app.api.routes.auth import router as auth_router
# from app.api.routes_transactions import router as tx_router
# from app.db.session import engine
# from app.db import models 
# from app.db.base import Base

# # 👇 ensures models are registered
# from app.db import models  # DO NOT REMOVE


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     await engine.dispose()


# app = FastAPI(
#     title="SentinelStream",
#     lifespan=lifespan
# )

# # ✅ Routers
# app.include_router(auth_router)   # /auth/*
# app.include_router(tx_router)     # /transactions/*


# @app.get("/")
# async def root():
#     return {"message": "SentinelStream API Running"}


# @app.get("/health")
# async def health():
#     return {"status": "ok"}
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes.auth import router as auth_router
from app.api.routes.transactions import router as tx_router

from app.db.session import engine
from app.db.base import Base
from app.db import models  # ensures models are registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="SentinelStream",
    lifespan=lifespan
)

# Routers
app.include_router(auth_router)
app.include_router(tx_router)


@app.get("/")
async def root():
    return {"message": "SentinelStream API Running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
