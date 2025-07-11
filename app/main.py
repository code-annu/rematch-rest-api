from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from .core.database import lifespan, get_db
from .model.user_model import UserCreate
from app.core.dependencies import get_user_repository
from .repository.user_repository import UserRepository

app = FastAPI(lifespan=lifespan)


@app.post("/")
async def add_user(new_user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)):
    return await user_repo.create_user(new_user)

