from fastapi import FastAPI
from contextlib import asynccontextmanager
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
ca = certifi.where()

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=ca)
    db.client = app.state.client
    app.state.db = app.state.client['rematch_db']
    await app.state.db.command("ping")
    db.database = db.client['rematch_db']
    yield
    app.state.client.close()

async def get_database():
    return db.database