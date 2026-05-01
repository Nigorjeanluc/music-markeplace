from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class GenreResponse(GenreBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
