from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.core.security import get_current_admin_user
from app.services.track_service import TrackService
from app.schemas.track import TrackCreate, TrackUpdate, TrackResponse
from app.schemas.pagination import PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[TrackResponse])
def list_tracks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    album_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List tracks with optional filters (public endpoint)."""
    track_service = TrackService(db)
    tracks, total = track_service.get_tracks(page=page, page_size=page_size, album_id=album_id, search=search)
    
    items = [
        TrackResponse(
            id=str(t.id),
            name=t.name,
            date=t.date,
            album_id=str(t.album_id),
            created_at=t.created_at,
        )
        for t in tracks
    ]
    total_pages = (total + page_size - 1) // page_size
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{track_id}", response_model=TrackResponse)
def get_track(track_id: str, db: Session = Depends(get_db)):
    """Get track detail (public endpoint)."""
    track_service = TrackService(db)
    track = track_service.get_track(track_id)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    return TrackResponse(
        id=str(track.id),
        name=track.name,
        date=track.date,
        album_id=str(track.album_id),
        created_at=track.created_at,
    )


@router.post("/", response_model=TrackResponse)
def create_track(
    track_in: TrackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Create a new track (admin only)."""
    track_service = TrackService(db)
    track = track_service.create_track(track_in)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )
    return TrackResponse(
        id=str(track.id),
        name=track.name,
        date=track.date,
        album_id=str(track.album_id),
        created_at=track.created_at,
    )


@router.put("/{track_id}", response_model=TrackResponse)
def update_track(
    track_id: str,
    track_in: TrackUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Update a track (admin only)."""
    track_service = TrackService(db)
    track = track_service.update_track(track_id, track_in)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    return TrackResponse(
        id=str(track.id),
        name=track.name,
        date=track.date,
        album_id=str(track.album_id),
        created_at=track.created_at,
    )


@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_track(
    track_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Delete a track (admin only)."""
    track_service = TrackService(db)
    if not track_service.delete_track(track_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
