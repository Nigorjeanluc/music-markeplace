from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Tuple

from app.models.playlist import Playlist
from app.models.playlist_track import PlaylistTrack
from app.models.track import Track
from app.models.album import Album
from app.models.artist import Artist
from app.schemas.playlist import PlaylistCreate, PlaylistUpdate, PlaylistResponse, PlaylistDetailResponse, TrackInPlaylist
from app.core.uuid_utils import is_valid_uuid


class PlaylistService:
    def __init__(self, db: Session):
        self.db = db

    def get_playlists(self, user_id: str) -> List[Playlist]:
        """Get all playlists for a user."""
        return self.db.query(Playlist).filter(Playlist.user_id == user_id).all()

    def get_playlist(self, playlist_id: str, user_id: str) -> Optional[Playlist]:
        """Get a playlist by ID, ensuring it belongs to the user."""
        if not is_valid_uuid(playlist_id) or not is_valid_uuid(user_id):
            return None
        return self.db.query(Playlist).filter(
            Playlist.id == playlist_id,
            Playlist.user_id == user_id
        ).first()

    def create_playlist(self, playlist_in: PlaylistCreate, user_id: str) -> Optional[Playlist]:
        """Create a new playlist with optional initial tracks."""
        if not is_valid_uuid(user_id):
            return None
        playlist = Playlist(
            name=playlist_in.name,
            user_id=user_id,
        )
        self.db.add(playlist)
        self.db.flush()  # Get playlist.id

        # Add initial tracks if provided
        for track_id in playlist_in.track_ids:
            if not is_valid_uuid(track_id):
                self.db.rollback()
                return None
            track = self.db.query(Track).filter(Track.id == track_id).first()
            if not track:
                self.db.rollback()
                return None

            playlist_track = PlaylistTrack(
                playlist_id=playlist.id,
                track_id=track_id,
            )
            self.db.add(playlist_track)

        self.db.commit()
        self.db.refresh(playlist)
        return playlist

    def update_playlist(self, playlist_id: str, playlist_in: PlaylistUpdate, user_id: str) -> Optional[Playlist]:
        """Update a playlist's name."""
        if not is_valid_uuid(playlist_id) or not is_valid_uuid(user_id):
            return None
        playlist = self.get_playlist(playlist_id, user_id)
        if not playlist:
            return None

        update_data = playlist_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(playlist, field, value)

        self.db.commit()
        self.db.refresh(playlist)
        return playlist

    def delete_playlist(self, playlist_id: str, user_id: str) -> bool:
        """Delete a playlist. Returns True if deleted, False if not found."""
        if not is_valid_uuid(playlist_id) or not is_valid_uuid(user_id):
            return False
        playlist = self.get_playlist(playlist_id, user_id)
        if not playlist:
            return False

        self.db.delete(playlist)
        self.db.commit()
        return True

    def add_track_to_playlist(self, playlist_id: str, track_id: str, user_id: str) -> Optional[bool]:
        """Add a track to a playlist. Returns None if playlist/track not found, False if track already exists."""
        if not is_valid_uuid(playlist_id) or not is_valid_uuid(track_id) or not is_valid_uuid(user_id):
            return None
        playlist = self.get_playlist(playlist_id, user_id)
        if not playlist:
            return None

        # Verify track exists
        track = self.db.query(Track).filter(Track.id == track_id).first()
        if not track:
            return None

        # Check if track already in playlist
        existing = self.db.query(PlaylistTrack).filter(
            PlaylistTrack.playlist_id == playlist_id,
            PlaylistTrack.track_id == track_id
        ).first()
        if existing:
            return False

        playlist_track = PlaylistTrack(
            playlist_id=playlist.id,
            track_id=track_id,
        )
        self.db.add(playlist_track)
        self.db.commit()
        return True

    def remove_track_from_playlist(self, playlist_id: str, track_id: str, user_id: str) -> bool:
        """Remove a track from a playlist. Returns True if removed, False if not found."""
        if not is_valid_uuid(playlist_id) or not is_valid_uuid(track_id) or not is_valid_uuid(user_id):
            return False
        playlist = self.get_playlist(playlist_id, user_id)
        if not playlist:
            return False

        playlist_track = self.db.query(PlaylistTrack).filter(
            PlaylistTrack.playlist_id == playlist_id,
            PlaylistTrack.track_id == track_id
        ).first()
        if not playlist_track:
            return False

        self.db.delete(playlist_track)
        self.db.commit()
        return True

    def get_playlist_track_count(self, playlist_id: str) -> int:
        """Get the number of tracks in a playlist."""
        if not is_valid_uuid(playlist_id):
            return 0
        return self.db.query(func.count(PlaylistTrack.id)).filter(
            PlaylistTrack.playlist_id == playlist_id
        ).scalar() or 0

    def get_playlist_tracks(self, playlist_id: str) -> List[TrackInPlaylist]:
        """Get all tracks in a playlist with album/artist info."""
        if not is_valid_uuid(playlist_id):
            return []
        tracks_query = (
            self.db.query(Track, Album, Artist)
            .join(PlaylistTrack, PlaylistTrack.track_id == Track.id)
            .join(Album, Track.album_id == Album.id)
            .join(Artist, Album.artist_id == Artist.id)
            .filter(PlaylistTrack.playlist_id == playlist_id)
            .all()
        )

        return [
            TrackInPlaylist(
                id=str(t.id),
                name=t.name,
                date=t.date,
                album_name=album.name,
                artist_name=artist.performing_name,
            )
            for t, album, artist in tracks_query
        ]

    def build_playlist_response(self, playlist: Playlist, include_tracks: bool = False) -> PlaylistResponse | PlaylistDetailResponse:
        """Build playlist response with track count and optional tracks."""
        track_count = self.get_playlist_track_count(playlist.id)

        if not include_tracks:
            return PlaylistResponse(
                id=str(playlist.id),
                name=playlist.name,
                created_at=playlist.created_at,
                track_count=track_count,
            )

        tracks = self.get_playlist_tracks(playlist.id)
        return PlaylistDetailResponse(
            id=str(playlist.id),
            name=playlist.name,
            created_at=playlist.created_at,
            track_count=track_count,
            tracks=tracks,
        )
