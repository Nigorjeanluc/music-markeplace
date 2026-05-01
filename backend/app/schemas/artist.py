from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional


class ArtistBase(BaseModel):
    real_name: str
    performing_name: str
    date_of_birth: date
    photo_url: str | None = None


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
    photo_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
