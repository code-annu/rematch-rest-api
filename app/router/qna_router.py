# app/routers/qna_router.py
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status
from app.model.qna_model import QnaCreate, QnaUpdate, QnaResponse
from app.repository.qna_repository import QnaRepository
from app.core.dependencies import get_qna_repository
from app.core.exception import ResourceNotFoundError, InvalidUpdateError

qna_router = APIRouter()


@qna_router.post("/add", response_model=QnaResponse, status_code=status.HTTP_201_CREATED)
async def add_qna(
        new_qna: QnaCreate,
        repo: QnaRepository = Depends(get_qna_repository),
):
    try:
        return await repo.create_qna(new_qna)
    except Exception as e:
        # Log error in production
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create QnA")


@qna_router.get("/get", response_model=QnaResponse)
async def get_qna(qid: str, repo: QnaRepository = Depends(get_qna_repository)):
    try:
        return await repo.get_qna(qid)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@qna_router.put("/update", response_model=QnaResponse)
async def update_qna(
        qid: str,
        update_data: QnaUpdate,
        repo: QnaRepository = Depends(get_qna_repository),
):
    try:
        return await repo.update_qna(qid, update_data)
    except InvalidId as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except InvalidUpdateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@qna_router.delete("/delete")
async def delete_qna(qid: str, repo: QnaRepository = Depends(get_qna_repository)):
    try:
        await repo.delete_qna(qid)
        return {"message": "QnA deleted successfully."}
    except InvalidId as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
