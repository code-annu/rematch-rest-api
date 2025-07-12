from watchfiles import awatch

from app.core.exception import InvalidUpdateError, ResourceNotFoundError
from app.model.user_model import *
from app.repository.user_repository import UserRepository
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_user_repository

user_router = APIRouter()


@user_router.post("/add")
async def add_new_user(new_user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)):
    try:
        await user_repo.get_user(uid=new_user.uid)
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    except ResourceNotFoundError:
        pass

    try:
        return await user_repo.create_user(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Something went wrong {e}")


@user_router.get("/get")
async def get_user_by_uid(uid: str, user_repo: UserRepository = Depends(get_user_repository)):
    try:
        return await user_repo.get_user(uid)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.put("/update")
async def update_user_by_uid(uid: str, update_user: UserUpdate,
                             user_repo: UserRepository = Depends(get_user_repository)):
    try:
        return await user_repo.update_user(uid=uid, update_user=update_user)
    except InvalidUpdateError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data is provided for update")
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.delete("/delete")
async def update_user_by_uid(uid: str, user_repo: UserRepository = Depends(get_user_repository)):
    try:
        await user_repo.delete_user(uid=uid)
        return {"message", "User deleted successfully."}
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.get("/all")
async def get_user_for(gender: str, min_birth_year: int, max_birth_year: int,
                       user_repo: UserRepository = Depends(get_user_repository)):
    return await user_repo.get_users(gender=gender, min_birth_year=min_birth_year, max_birth_year=max_birth_year)
