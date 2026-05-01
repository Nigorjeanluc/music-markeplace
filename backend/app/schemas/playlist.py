from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID


class PlaylistBase(BaseModel):
    name: str


class PlaylistCreate(PlaylistBase):
    track_ids: List[str] = []


class PlaylistUpdate(BaseModel):
    name: Optional[str] = None


class PlaylistTrackAdd(BaseModel):
    track_id: str


class TrackInPlaylist(BaseModel):
    id: str
    name: str
    date: date
    album_name: str
    artist_name: str

    model_config = ConfigDict(from_attributes=True)


class PlaylistResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    track_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class PlaylistDetailResponse(PlaylistResponse):
    tracks: List[TrackInPlaylist] = []
