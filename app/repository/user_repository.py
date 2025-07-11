from fastapi import Query
from motor.motor_asyncio import AsyncIOMotorCollection
from app.model.user_model import *
from app.core.exception import *


class UserRepository:
    def __init__(self, user_collection: AsyncIOMotorCollection):
        self.user_collection = user_collection

    async def create_user(self, new_user: UserCreate) -> UserResponse:
        data = new_user.model_dump()
        result = await self.user_collection.insert_one(data)
        data["id"] = str(result.inserted_id)
        return UserResponse(**data)

    async def get_user(self, uid: str) -> UserResponse:
        doc = await self.user_collection.find_one({"uid": uid})
        if not doc:
            raise ResourceNotFoundError(f"User {uid} not found")
        return UserResponse(**doc)

    async def update_user(self, uid: str, update_user: UserUpdate) -> UserResponse:
        data = update_user.model_dump(exclude_unset=True)
        if not data:
            raise InvalidUpdateError("No fields to update")

        result = await self.user_collection.update_one(
            {"uid": uid}, {"$set": data}
        )
        if result.matched_count == 0:
            raise ResourceNotFoundError(f"User {uid} not found")

        return await self.get_user(uid)

    async def delete_user(self, uid: str) -> None:
        result = await self.user_collection.delete_one({"uid": uid})
        if result.deleted_count == 0:
            raise ResourceNotFoundError(f"User {uid} not found")

    async def get_users(
            self,
            min_birth_year: Optional[int] = Query(None, alias="birth_year_gte"),
            max_birth_year: Optional[int] = Query(None, alias="birth_year_lte"),
            gender: Optional[str] = None
    ) -> list[UserResponse]:
        query = {}
        if min_birth_year is not None:
            query.setdefault("birth_year", {})["$gte"] = min_birth_year
        if max_birth_year is not None:
            query.setdefault("birth_year", {})["$lte"] = max_birth_year
        if gender:
            query["gender"] = gender

        docs = await self.user_collection.find(query).to_list(length=None)
        users: list[UserResponse] = []
        for doc in docs:
            doc["id"] = str(doc.pop("_id"))
            users.append(UserResponse(**doc))
        return users
