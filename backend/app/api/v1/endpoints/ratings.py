from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.album import Album
from app.services.rating_service import RatingService
from app.schemas.rating import RatingCreate, RatingUpdate, RatingResponse

router = APIRouter()


@router.post("/", response_model=RatingResponse)
def rate_album(
    rating_in: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Rate an album (must have purchased it first)."""
    rating_service = RatingService(db)
    result = rating_service.create_or_update_rating(current_user.id, rating_in)
    if not result:
        # Check if album exists
        album = db.query(Album).filter(Album.id == rating_in.album_id).first()
        if not album:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album not found"
            )
        # Check if user purchased the album
        from app.models.purchase import Purchase
        purchase = db.query(Purchase).filter(
            Purchase.user_id == current_user.id,
            Purchase.album_id == rating_in.album_id
        ).first()
        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You must purchase the album before rating it"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )

    rating_obj, avg_rating = result
    album = db.query(Album).filter(Album.id == rating_in.album_id).first()
    return rating_service.build_rating_response(rating_obj, album.name if album else "", avg_rating)


@router.put("/{album_id}", response_model=RatingResponse)
def update_rating(
    album_id: str,
    rating_in: RatingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update user's rating for an album."""
    rating_service = RatingService(db)
    result = rating_service.update_rating(current_user.id, album_id, rating_in)
    if not result:
        # Check if rating exists or rating is invalid
        from app.models.rating import Rating
        rating_obj = db.query(Rating).filter(
            Rating.user_id == current_user.id,
            Rating.album_id == album_id
        ).first()
        if not rating_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rating not found. You must create a rating first."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )

    rating_obj, avg_rating = result
    album = db.query(Album).filter(Album.id == album_id).first()
    return rating_service.build_rating_response(rating_obj, album.name if album else "", avg_rating)


@router.get("/me", response_model=List[RatingResponse])
def get_my_ratings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's ratings."""
    rating_service = RatingService(db)
    ratings_data = rating_service.get_user_ratings(current_user.id)

    return [
        rating_service.build_rating_response(r, a.name if a else "", avg)
        for r, a, avg in ratings_data
    ]


@router.get("/album/{album_id}", response_model=List[RatingResponse])
def get_album_ratings(
    album_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all ratings for an album + average (public endpoint). Supports pagination."""
    rating_service = RatingService(db)
    result = rating_service.get_album_ratings(album_id, skip=skip, limit=limit)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )

    rating_responses, _ = result
    return rating_responses
