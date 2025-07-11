from typing import Optional

from pydantic import BaseModel


class QnaCreate(BaseModel):
    breakup_reason: str
    pain_rate: int
    relationship_length: int  # In months
    coping_mechanism: str


class QnaUpdate(BaseModel):
    breakup_reason: Optional[str] = None
    pain_rate: Optional[int] = None
    relationship_length: Optional[int] = None
    coping_mechanism: Optional[str] = None


class QnaResponse(BaseModel):
    id: str
    breakup_reason: str
    pain_rate: int
    relationship_length: int
    coping_mechanism: str
