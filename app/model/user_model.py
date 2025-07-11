from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    uid: str
    first_name: str
    last_name: str
    dob: str
    gender: str
    bub_id: str | None = None
    qna_id: str | None = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    bub_id: Optional[str] = None
    qna_id: Optional[str] = None

class UserResponse(BaseModel):
    uid: str
    first_name: str
    last_name: str
    dob: str
    gender: str
    bub_id: str | None = None
    qna_id: str | None = None