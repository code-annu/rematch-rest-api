from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from app.model.qna_model import QnaCreate, QnaUpdate, QnaResponse
from app.core.exception import ResourceNotFoundError, InvalidUpdateError

class QnaRepository:
    def __init__(self, qna_collection: AsyncIOMotorCollection):
        self.qna_collection = qna_collection

    async def create_qna(self, new_qna: QnaCreate) -> QnaResponse:
        data = new_qna.model_dump()
        result = await self.qna_collection.insert_one(data)
        data["id"] = str(result.inserted_id)
        return QnaResponse(**data)

    async def get_qna(self, qid: str) -> QnaResponse:
        doc = await self.qna_collection.find_one({"_id": ObjectId(qid)})
        if not doc:
            raise ResourceNotFoundError(f"QnA {qid} not found")
        doc['id'] = qid
        return QnaResponse(**doc)

    async def update_qna(self, qid: str, qna_update: QnaUpdate) -> QnaResponse:
        data = qna_update.model_dump(exclude_unset=True)
        if not data:
            raise InvalidUpdateError("No fields to update")

        result = await self.qna_collection.update_one(
            {"_id": ObjectId(qid)}, {"$set": data}
        )
        if result.matched_count == 0:
            raise ResourceNotFoundError(f"QnA {qid} not found")

        return await self.get_qna(qid)

    async def delete_qna(self, qid: str) -> None:
        result = await self.qna_collection.delete_one({"_id": ObjectId(qid)})
        if result.deleted_count == 0:
            raise ResourceNotFoundError(f"QnA {qid} not found")
