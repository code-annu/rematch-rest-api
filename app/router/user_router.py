from app.core.exception import InvalidUpdateError, ResourceNotFoundError
from app.model.user_model import *
from app.repository.user_repository import UserRepository
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_user_repository

user_router = APIRouter()


@user_router.post("/add")
async def add_new_user(new_user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)):
    try:
        return await user_repo.create_user(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong.")


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
        return {"message","User deleted successfully."}
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
