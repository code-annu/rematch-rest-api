from motor.motor_asyncio import AsyncIOMotorCollection
from app.model.user_model import UserCreate, UserResponse

class UserRepository:
    def __init__(self, user_collection: AsyncIOMotorCollection):
        self.user_collection = user_collection

    async def create_user(self, new_user: UserCreate) -> UserResponse:
        new_user_dict = new_user.model_dump()
        result = await self.user_collection.insert_one(new_user_dict)
        new_user_dict["id"] = str(result.inserted_id)
        return UserResponse(**new_user_dict)
