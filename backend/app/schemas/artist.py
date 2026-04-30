from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ArtistBase(BaseModel):
    real_name: str
    performing_name: str
    date_of_birth: date


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    real_name: Optional[str] = None
    performing_name: Optional[str] = None
    date_of_birth: Optional[date] = None


class ArtistResponse(ArtistBase):
    id: str
    created_at: datetime
    album_count: int = 0

    class Config:
        from_attributes = True
