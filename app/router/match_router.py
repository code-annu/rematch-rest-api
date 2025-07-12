from app.core.dependencies import get_user_repository, get_qna_repository
from app.model.user_model import UserResponse
from app.repository.qna_repository import QnaRepository
from app.repository.user_repository import UserRepository
from app.router.qna_router import qna_router
from app.service.bub_service import match_me
from fastapi import APIRouter, Depends

match_router = APIRouter()


@match_router.post("/find")
async def find_my_bub(user: UserResponse, gender: str, min_birth_year: int, max_birth_year: int,
                      user_repo: UserRepository = Depends(get_user_repository),
                      qna_repo: QnaRepository = Depends(get_qna_repository)):
    user, score = await match_me(me=user, gender=gender, min_birth_year=min_birth_year,
                                 max_birth_year=max_birth_year, user_repo=user_repo, qna_repo=qna_repo)
    print(f"Your score is {score}")
    return user
