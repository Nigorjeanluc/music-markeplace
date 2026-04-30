from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class RatingCreate(BaseModel):
    album_id: str
    rating: int  # 1-5


class RatingUpdate(BaseModel):
    rating: int  # 1-5


class RatingResponse(BaseModel):
    album_id: str
    album_name: str
    user_rating: int
    avg_rating: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True
