from fastapi import APIRouter, Depends

from app.core.dependencies import get_user_repository, get_qna_repository
from app.repository.qna_repository import QnaRepository
from app.repository.user_repository import UserRepository
from app.service.bub_service import match_me

match_router = APIRouter()


@match_router.post("/find")
async def find_my_bub(user_uid: str, gender: str, min_birth_year: int, max_birth_year: int,
                      user_repo: UserRepository = Depends(get_user_repository),
                      qna_repo: QnaRepository = Depends(get_qna_repository)):
    user, score = await match_me(user_uid=user_uid, gender=gender, min_birth_year=min_birth_year,
                                 max_birth_year=max_birth_year, user_repo=user_repo, qna_repo=qna_repo)
    print(f"Your score is {score}")
    return user
