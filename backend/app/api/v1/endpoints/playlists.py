from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.playlist_service import PlaylistService
from app.schemas.playlist import (
    PlaylistCreate, PlaylistUpdate, PlaylistResponse,
    PlaylistDetailResponse, PlaylistTrackAdd
)

router = APIRouter()


@router.get("/", response_model=List[PlaylistResponse])
def list_playlists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List current user's playlists."""
    playlist_service = PlaylistService(db)
    playlists = playlist_service.get_playlists(current_user.id)
    return [playlist_service.build_playlist_response(p, include_tracks=False) for p in playlists]


@router.get("/{playlist_id}", response_model=PlaylistDetailResponse)
def get_playlist(
    playlist_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get playlist detail with tracks."""
    playlist_service = PlaylistService(db)
    playlist = playlist_service.get_playlist(playlist_id, current_user.id)
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    return playlist_service.build_playlist_response(playlist, include_tracks=True)


@router.post("/", response_model=PlaylistDetailResponse)
def create_playlist(
    playlist_in: PlaylistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new playlist."""
    playlist_service = PlaylistService(db)
    playlist = playlist_service.create_playlist(playlist_in, current_user.id)
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    return playlist_service.build_playlist_response(playlist, include_tracks=True)


@router.put("/{playlist_id}", response_model=PlaylistResponse)
def update_playlist(
    playlist_id: str,
    playlist_in: PlaylistUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update playlist name."""
    playlist_service = PlaylistService(db)
    playlist = playlist_service.update_playlist(playlist_id, playlist_in, current_user.id)
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    return playlist_service.build_playlist_response(playlist, include_tracks=False)


@router.post("/{playlist_id}/tracks", status_code=status.HTTP_204_NO_CONTENT)
def add_track_to_playlist(
    playlist_id: str,
    track_in: PlaylistTrackAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add a track to a playlist."""
    playlist_service = PlaylistService(db)
    result = playlist_service.add_track_to_playlist(playlist_id, track_in.track_id, current_user.id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist or track not found"
        )
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Track already in playlist"
        )


@router.delete("/{playlist_id}/tracks/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_track_from_playlist(
    playlist_id: str,
    track_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove a track from a playlist."""
    playlist_service = PlaylistService(db)
    if not playlist_service.remove_track_from_playlist(playlist_id, track_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist or track not found"
        )


@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(
    playlist_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a playlist."""
    playlist_service = PlaylistService(db)
    if not playlist_service.delete_playlist(playlist_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
