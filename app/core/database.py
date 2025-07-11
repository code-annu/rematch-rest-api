import os
from contextlib import asynccontextmanager
import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from fastapi import FastAPI, Depends
import logging
from dotenv import load_dotenv
from starlette.requests import Request

load_dotenv()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
    db = client["rematch_db"]
    ping = await db.command("ping")
    if ping.get("ok") != 1:
        raise RuntimeError("🚨 Cannot connect to MongoDB Atlas")
    logger.info("✅ MongoDB connected via Atlas")

    # Attach to app state
    app.state.mongodb_client = client
    app.state.db = db

    yield  # App is running

    # Shutdown: close client
    client.close()
    logger.info("🛑 MongoDB connection closed")


def get_db(request: Request) -> AsyncIOMotorDatabase:
    return request.app.state.db


def get_collection(name: str):
    def _get_collection(db=Depends(get_db)) -> AsyncIOMotorCollection:
        return db[name]

    return _get_collection
