from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PurchaseCreate(BaseModel):
    album_id: str


class PurchaseResponse(BaseModel):
    id: str
    album_id: str
    album_name: str
    artist_name: str
    purchase_date: datetime
    amount_paid: float

    class Config:
        from_attributes = True
