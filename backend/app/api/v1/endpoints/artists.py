from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.core.security import get_current_admin_user
from app.services.artist_service import ArtistService
from app.schemas.artist import ArtistCreate, ArtistUpdate, ArtistResponse

router = APIRouter()


@router.get("/", response_model=List[ArtistResponse])
def list_artists(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List artists with optional search."""
    artist_service = ArtistService(db)
    artists_data = artist_service.get_artists(skip=skip, limit=limit, search=search)

    result = []
    for artist, album_count in artists_data:
        artist_data = ArtistResponse(
            id=str(artist.id),
            real_name=artist.real_name,
            performing_name=artist.performing_name,
            date_of_birth=artist.date_of_birth,
            created_at=artist.created_at,
            album_count=album_count
        )
        result.append(artist_data)
    return result


@router.get("/{artist_id}", response_model=ArtistResponse)
def get_artist(artist_id: str, db: Session = Depends(get_db)):
    """Get artist detail with album count."""
    artist_service = ArtistService(db)
    artist_data = artist_service.get_artist(artist_id)
    if not artist_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )

    artist, album_count = artist_data
    return ArtistResponse(
        id=str(artist.id),
        real_name=artist.real_name,
        performing_name=artist.performing_name,
        date_of_birth=artist.date_of_birth,
        created_at=artist.created_at,
        album_count=album_count
    )


@router.post("/", response_model=ArtistResponse)
def create_artist(
    artist_in: ArtistCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Create a new artist (admin only)."""
    artist_service = ArtistService(db)
    artist = artist_service.create_artist(artist_in)
    return ArtistResponse(
        id=str(artist.id),
        real_name=artist.real_name,
        performing_name=artist.performing_name,
        date_of_birth=artist.date_of_birth,
        created_at=artist.created_at,
        album_count=0  # New artist has no albums yet
    )


@router.put("/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: str,
    artist_in: ArtistUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Update an artist (admin only)."""
    artist_service = ArtistService(db)
    artist = artist_service.update_artist(artist_id, artist_in)
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )

    # Get updated album count
    album_count = db.query(Album).filter(Album.artist_id == artist.id).count()
    return ArtistResponse(
        id=str(artist.id),
        real_name=artist.real_name,
        performing_name=artist.performing_name,
        date_of_birth=artist.date_of_birth,
        created_at=artist.created_at,
        album_count=album_count
    )


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artist(
    artist_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Delete an artist (admin only)."""
    artist_service = ArtistService(db)
    if not artist_service.delete_artist(artist_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
