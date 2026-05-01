from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID


class AlbumBase(BaseModel):
    name: str
    price: float
    release_date: Optional[date] = None
    artist_id: str
    genre_ids: List[str] = []
    cover_image_url: str | None = None


class AlbumCreate(AlbumBase):
    pass


class AlbumUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    release_date: Optional[date] = None
    genre_ids: Optional[List[str]] = None


class AlbumResponse(BaseModel):
    id: str
    name: str
    price: float
    release_date: Optional[date] = None
    artist_id: str
    artist_name: str
    rating: Optional[float] = None
    genre_names: List[str] = []
    cover_image_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
