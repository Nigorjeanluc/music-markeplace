from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List, Optional

from app.db.session import get_db
from app.core.security import get_current_admin_user
from app.services.album_service import AlbumService
from app.schemas.album import AlbumCreate, AlbumUpdate, AlbumResponse
from app.models.album import Album
from app.models.artist import Artist
from app.models.genre import Genre
from app.models.album_genres import AlbumGenre
from app.models.rating import Rating
from app.models.purchase import Purchase

router = APIRouter()


def get_album_rating_subquery():
    """Subquery to compute average rating from purchasers only."""
    return (
        select(func.avg(Rating.rating))
        .join(Purchase, (Rating.user_id == Purchase.user_id) & (Rating.album_id == Purchase.album_id))
        .where(Rating.album_id == Album.id)
        .correlate(Album)
        .scalar_subquery()
    )


@router.get("/", response_model=List[AlbumResponse])
def list_albums(
    skip: int = 0,
    limit: int = 100,
    artist_id: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List albums with filters (public endpoint)."""
    album_service = AlbumService(db)
    albums_data = album_service.get_albums(skip=skip, limit=limit, artist_id=artist_id, genre=genre, search=search)

    result = []
    for album, avg_rating, genre_names, artist in albums_data:
        result.append(AlbumResponse(
            id=str(album.id),
            name=album.name,
            price=float(album.price),
            release_date=album.release_date,
            artist_id=str(album.artist_id),
            artist_name=artist.performing_name if artist else "",
            rating=float(avg_rating) if avg_rating else None,
            genre_names=genre_names,
            created_at=album.created_at,
            updated_at=album.updated_at,
        ))
    return result


@router.get("/{album_id}", response_model=AlbumResponse)
def get_album(album_id: str, db: Session = Depends(get_db)):
    """Get album detail with rating (public endpoint)."""
    album_service = AlbumService(db)
    album_data = album_service.get_album(album_id)
    if not album_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )

    album, avg_rating, genre_names, artist = album_data

    return AlbumResponse(
        id=str(album.id),
        name=album.name,
        price=float(album.price),
        release_date=album.release_date,
        artist_id=str(album.artist_id),
        artist_name=artist.performing_name if artist else "",
        rating=float(avg_rating) if avg_rating else None,
        genre_names=genre_names,
        created_at=album.created_at,
        updated_at=album.updated_at,
    )


@router.post("/", response_model=AlbumResponse)
def create_album(
    album_in: AlbumCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Create a new album (admin only)."""
    album_service = AlbumService(db)
    album = album_service.create_album(album_in)
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )

    # Get artist name for response
    artist = db.query(Artist).filter(Artist.id == album.artist_id).first()

    # Get genre names for response
    genre_names = [
        g.name for g in
        db.query(Genre).join(AlbumGenre, AlbumGenre.genre_id == Genre.id).filter(AlbumGenre.album_id == album.id).all()
    ]

    return AlbumResponse(
        id=str(album.id),
        name=album.name,
        price=float(album.price),
        release_date=album.release_date,
        artist_id=str(album.artist_id),
        artist_name=artist.performing_name if artist else "",
        rating=None,
        genre_names=genre_names,
        created_at=album.created_at,
        updated_at=album.updated_at,
    )


@router.put("/{album_id}", response_model=AlbumResponse)
def update_album(
    album_id: str,
    album_in: AlbumUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Update an album (admin only)."""
    album_service = AlbumService(db)
    album = album_service.update_album(album_id, album_in)
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )

    # Compute rating
    rating_subq = album_service._get_album_rating_subquery()
    avg_rating = db.query(rating_subq).filter(Album.id == album_id).scalar()

    # Get genre names
    genre_names = [
        g.name for g in
        db.query(Genre).join(AlbumGenre, AlbumGenre.genre_id == Genre.id).filter(AlbumGenre.album_id == album_id).all()
    ]
    artist = db.query(Artist).filter(Artist.id == album.artist_id).first()

    return AlbumResponse(
        id=str(album.id),
        name=album.name,
        price=float(album.price),
        release_date=album.release_date,
        artist_id=str(album.artist_id),
        artist_name=artist.performing_name if artist else "",
        rating=float(avg_rating) if avg_rating else None,
        genre_names=genre_names,
        created_at=album.created_at,
        updated_at=album.updated_at,
    )


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(
    album_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Delete an album (admin only)."""
    album_service = AlbumService(db)
    if not album_service.delete_album(album_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )
