from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Tuple

from app.models.purchase import Purchase
from app.models.album import Album
from app.models.artist import Artist
from app.models.rating import Rating
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.core.uuid_utils import is_valid_uuid


class PurchaseService:
    def __init__(self, db: Session):
        self.db = db

    def create_purchase(self, user_id: str, purchase_in: PurchaseCreate) -> Optional[Purchase]:
        """Purchase an album. Returns None if album not found."""
        if not is_valid_uuid(user_id) or not is_valid_uuid(purchase_in.album_id):
            return None
        album = self.db.query(Album).filter(Album.id == purchase_in.album_id).first()
        if not album:
            return None

        purchase = Purchase(
            user_id=user_id,
            album_id=purchase_in.album_id,
            amount_paid=album.price,
        )

        self.db.add(purchase)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return None  # Album already purchased
        self.db.refresh(purchase)
        return purchase

    def get_user_purchases(
        self, user_id: str, page: int = 1, page_size: int = 20
    ) -> Tuple[List[Tuple[Purchase, Album, Optional[Artist], Optional[float], Optional[float]]], int]:
        """Get all purchases for a user with album, artist, user rating, and avg rating. With pagination."""
        if not is_valid_uuid(user_id):
            return ([], 0)
        query = self.db.query(Purchase).filter(Purchase.user_id == user_id)
        total = query.count()
        skip = (page - 1) * page_size
        purchases = query.offset(skip).limit(page_size).all()

        result = []
        for purchase in purchases:
            album = self.db.query(Album).filter(Album.id == purchase.album_id).first()
            if not album:
                continue
            artist = self.db.query(Artist).filter(Artist.id == album.artist_id).first()

            # Get user's rating for this album
            user_rating = self.db.query(Rating).filter(
                Rating.user_id == user_id,
                Rating.album_id == purchase.album_id
            ).first()

            # Get average rating
            avg_rating = self.db.query(func.avg(Rating.rating)).filter(
                Rating.album_id == purchase.album_id
            ).scalar()

            result.append((purchase, album, artist, user_rating, avg_rating))
        return (result, total)

    def build_purchase_response(self, purchase: Purchase, album: Album, artist: Optional[Artist]) -> PurchaseResponse:
        """Build PurchaseResponse from purchase, album, and artist."""
        return PurchaseResponse(
            id=str(purchase.id),
            album_id=str(purchase.album_id),
            album_name=album.name,
            artist_name=artist.performing_name if artist else "",
            purchase_date=purchase.purchase_date,
            amount_paid=float(purchase.amount_paid),
        )

    def build_purchase_response_with_ratings(
        self,
        purchase: Purchase,
        album: Album,
        artist: Optional[Artist],
        user_rating: Optional[Rating],
        avg_rating: Optional[float]
    ) -> dict:
        """Build extended purchase response including ratings."""
        return {
            "id": str(purchase.id),
            "album_id": str(purchase.album_id),
            "album_name": album.name,
            "artist_name": artist.performing_name if artist else "",
            "purchase_date": purchase.purchase_date,
            "amount_paid": float(purchase.amount_paid),
            "user_rating": user_rating.rating if user_rating else None,
            "avg_rating": float(avg_rating) if avg_rating else None,
        }
