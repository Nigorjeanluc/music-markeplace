from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional
from uuid import UUID


class TrackBase(BaseModel):
    name: str
    date: date
    album_id: str


class TrackCreate(TrackBase):
    pass


class TrackUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[date] = None
    album_id: Optional[str] = None


class TrackResponse(TrackBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
