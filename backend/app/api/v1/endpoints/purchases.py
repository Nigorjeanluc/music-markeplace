from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.album import Album
from app.models.artist import Artist
from app.services.purchase_service import PurchaseService
from app.schemas.purchase import PurchaseCreate, PurchaseResponse

router = APIRouter()


@router.post("/", response_model=PurchaseResponse)
def purchase_album(
    purchase_in: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Purchase an album (direct purchase, no cart)."""
    purchase_service = PurchaseService(db)
    purchase = purchase_service.create_purchase(current_user.id, purchase_in)
    if not purchase:
        # Check if album exists
        album = db.query(Album).filter(Album.id == purchase_in.album_id).first()
        if not album:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album not found"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Album already purchased"
        )

    album = db.query(Album).filter(Album.id == purchase.album_id).first()
    artist = db.query(Artist).filter(Artist.id == album.artist_id).first()
    return purchase_service.build_purchase_response(purchase, album, artist)


@router.get("/me/library", response_model=List[PurchaseResponse])
def get_library(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's purchased albums (personal library)."""
    purchase_service = PurchaseService(db)
    purchases_data = purchase_service.get_user_purchases(current_user.id)

    return [
        purchase_service.build_purchase_response_with_ratings(p, a, ar, ur, avg)
        for p, a, ar, ur, avg in purchases_data
    ]
