from app.matcher.match_me import measure_qna_similarity
from app.model.user_model import *
from app.repository.qna_repository import QnaRepository
from app.repository.user_repository import UserRepository


async def match_me(user_uid: str, min_birth_year: int, max_birth_year: int,
                   gender: str, user_repo: UserRepository, qna_repo: QnaRepository) -> tuple[
    UserResponse, float]:
    me = await user_repo.get_user(user_uid)
    users = await user_repo.get_users(min_birth_year=min_birth_year, max_birth_year=max_birth_year,
                                      gender=gender)
    best_score = -1
    bub = None
    for user in users:
        my_qna = await qna_repo.get_qna(me.qna_id)
        user_qna = await qna_repo.get_qna(user.qna_id)
        score = measure_qna_similarity(target_qna=my_qna, buddy_qna=user_qna)
        if score > best_score:
            best_score = score
            bub = user
    return bub, best_score
