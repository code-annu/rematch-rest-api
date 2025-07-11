from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.database import get_collection
from app.repository.qna_repository import QnaRepository
from app.repository.user_repository import UserRepository


def get_user_repository(
        users_col: AsyncIOMotorCollection = Depends(get_collection("users")),
) -> UserRepository:
    return UserRepository(users_col)


def get_qna_repository(
        qna_col: AsyncIOMotorCollection = Depends(get_collection("qna")),
) -> QnaRepository:
    return QnaRepository(qna_col)
