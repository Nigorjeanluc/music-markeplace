from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Tuple

from app.models.rating import Rating
from app.models.purchase import Purchase
from app.models.album import Album
from app.schemas.rating import RatingCreate, RatingUpdate, RatingResponse
from app.core.uuid_utils import is_valid_uuid


class RatingService:
    def __init__(self, db: Session):
        self.db = db

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
        if rating_in.rating < 1 or rating_in.rating > 5:
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
            )
            self.db.add(rating_obj)
            try:
                self.db.commit()
            except IntegrityError:
                self.db.rollback()
                return None
            self.db.refresh(rating_obj)

        # Get average rating
        avg_rating = self.db.query(func.avg(Rating.rating)).filter(
            Rating.album_id == rating_in.album_id
        ).scalar()

        return (rating_obj, float(avg_rating) if avg_rating else None)

    def update_rating(self, user_id: str, album_id: str, rating_in: RatingUpdate) -> Optional[Tuple[Rating, float]]:
        """Update user's rating for an album. Returns (rating, avg_rating) or None if not found/invalid."""
        if not is_valid_uuid(user_id) or not is_valid_uuid(album_id):
            return None
        # Validate rating range
        if rating_in.rating < 1 or rating_in.rating > 5:
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

        # Get average rating
        avg_rating = self.db.query(func.avg(Rating.rating)).filter(
            Rating.album_id == album_id
        ).scalar()

        return (rating_obj, float(avg_rating) if avg_rating else None)

    def get_user_ratings(self, user_id: str) -> List[Tuple[Rating, Album, Optional[float]]]:
        """Get all ratings by a user with album and avg rating."""
        if not is_valid_uuid(user_id):
            return []
        ratings = self.db.query(Rating).filter(Rating.user_id == user_id).all()

        result = []
        for r in ratings:
            album = self.db.query(Album).filter(Album.id == r.album_id).first()
            # Get average rating
            avg_rating = self.db.query(func.avg(Rating.rating)).filter(
                Rating.album_id == r.album_id
            ).scalar()

            result.append((r, album, float(avg_rating) if avg_rating else None))
        return result

    def get_album_ratings(self, album_id: str) -> Optional[Tuple[List[Rating], Album, Optional[float]]]:
        """Get all ratings for an album. Returns (ratings, album, avg_rating) or None if album not found."""
        if not is_valid_uuid(album_id):
            return None
        album = self.db.query(Album).filter(Album.id == album_id).first()
        if not album:
            return None

        ratings = self.db.query(Rating).filter(Rating.album_id == album_id).all()

        # Get average rating
        avg_rating = self.db.query(func.avg(Rating.rating)).filter(
            Rating.album_id == album_id
        ).scalar()

        return (ratings, album, float(avg_rating) if avg_rating else None)

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
