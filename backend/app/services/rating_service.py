from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Tuple
from datetime import datetime, timezone

from app.models.rating import Rating
from app.models.purchase import Purchase
from app.models.album import Album
from app.schemas.rating import RatingCreate, RatingUpdate, RatingResponse
from app.core.uuid_utils import is_valid_uuid


class RatingService:
    def __init__(self, db: Session):
        self.db = db

    def _get_avg_rating(self, album_id: str) -> Optional[float]:
        """Get average rating for an album."""
        avg = self.db.query(func.avg(Rating.rating)).filter(
            Rating.album_id == album_id
        ).scalar()
        return float(avg) if avg else None

    def create_or_update_rating(self, user_id: str, rating_in: RatingCreate) -> Optional[Tuple[Rating, float]]:
        """Rate an album (must have purchased it first). Returns (rating, avg_rating) or None if invalid."""
        if not is_valid_uuid(user_id) or not is_valid_uuid(rating_in.album_id):
            return None
        # Verify album exists
        album = self.db.query(Album).filter(Album.id == rating_in.album_id).first()
        if not album:
            return None

        # Verify user purchased the album
        purchase = self.db.query(Purchase).filter(
            Purchase.user_id == user_id,
            Purchase.album_id == rating_in.album_id
        ).first()
        if not purchase:
            return None

        # Validate rating range
        if not (1 <= rating_in.rating <= 5):
            return None

        # Upsert: try to insert, if duplicate then update
        existing = self.db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.album_id == rating_in.album_id
        ).first()

        if existing:
            existing.rating = rating_in.rating
            self.db.commit()
            self.db.refresh(existing)
            rating_obj = existing
        else:
            rating_obj = Rating(
                user_id=user_id,
                album_id=rating_in.album_id,
                rating=rating_in.rating,
                created_at=datetime.now(timezone.utc),
            )
            self.db.add(rating_obj)
            try:
                self.db.commit()
            except IntegrityError:
                self.db.rollback()
                return None
            self.db.refresh(rating_obj)

        avg_rating = self._get_avg_rating(rating_in.album_id)
        return (rating_obj, avg_rating)

    def update_rating(self, user_id: str, album_id: str, rating_in: RatingUpdate) -> Optional[Tuple[Rating, float]]:
        """Update user's rating for an album. Returns (rating, avg_rating) or None if not found/invalid."""
        if not is_valid_uuid(user_id) or not is_valid_uuid(album_id):
            return None
        # Validate rating range
        if not (1 <= rating_in.rating <= 5):
            return None

        # Find existing rating
        rating_obj = self.db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.album_id == album_id
        ).first()
        if not rating_obj:
            return None

        rating_obj.rating = rating_in.rating
        self.db.commit()
        self.db.refresh(rating_obj)

        avg_rating = self._get_avg_rating(album_id)
        return (rating_obj, avg_rating)

    def get_user_ratings(
        self, user_id: str, page: int = 1, page_size: int = 20
    ) -> Tuple[List[Tuple[Rating, str, Optional[float]]], int]:
        """Get all ratings by a user with album name and avg rating. With pagination."""
        if not is_valid_uuid(user_id):
            return ([], 0)
        query = self.db.query(Rating).filter(Rating.user_id == user_id)
        total = query.count()
        skip = (page - 1) * page_size
        ratings = query.offset(skip).limit(page_size).all()

        result = []
        for r in ratings:
            album = self.db.query(Album).filter(Album.id == r.album_id).first()
            album_name = album.name if album else "Unknown"
            avg_rating = self._get_avg_rating(r.album_id)
            result.append((r, album_name, avg_rating))
        return (result, total)
    def get_album_ratings(
        self, album_id: str, page: int = 1, page_size: int = 20
    ) -> Optional[Tuple[List[RatingResponse], Optional[float], int]]:
        """Get all ratings for an album with pagination. Returns (ratings, avg_rating, total) or None."""
        if not is_valid_uuid(album_id):
            return None
        album = self.db.query(Album).filter(Album.id == album_id).first()
        if not album:
            return None

        query = self.db.query(Rating).filter(Rating.album_id == album_id)
        total = query.count()
        skip = (page - 1) * page_size
        ratings = query.offset(skip).limit(page_size).all()

        avg_rating = self._get_avg_rating(album_id)

        rating_responses = [
            RatingResponse(
                album_id=str(r.album_id),
                album_name=album.name,
                user_rating=r.rating,
                avg_rating=avg_rating,
                created_at=r.created_at,
            )
            for r in ratings
        ]

        return (rating_responses, avg_rating, total)
    def build_rating_response(
        self, rating: Rating, album_name: str, avg_rating: Optional[float]
    ) -> RatingResponse:
        """Build RatingResponse from rating, album name, and avg rating."""
        return RatingResponse(
            album_id=str(rating.album_id),
            album_name=album_name,
            user_rating=rating.rating,
            avg_rating=avg_rating,
            created_at=rating.created_at,
        )
