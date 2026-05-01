from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.track import Track
from app.models.album import Album
from app.schemas.track import TrackCreate, TrackUpdate
from app.core.uuid_utils import is_valid_uuid


class TrackService:
    def __init__(self, db: Session):
        self.db = db

    def get_tracks(
        self,
        skip: int = 0,
        limit: int = 100,
        album_id: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Track]:
        """Get tracks with optional filters."""
        query = self.db.query(Track)
        if album_id:
            if not is_valid_uuid(album_id):
                return []
            query = query.filter(Track.album_id == album_id)
        if search:
            query = query.filter(Track.name.ilike(f"%{search}%"))
        return query.order_by(Track.date).offset(skip).limit(limit).all()

    def get_track(self, track_id: str) -> Optional[Track]:
        """Get a track by ID."""
        if not is_valid_uuid(track_id):
            return None
        return self.db.query(Track).filter(Track.id == track_id).first()

    def create_track(self, track_in: TrackCreate) -> Track:
        """Create a new track."""
        # Verify album exists
        if not is_valid_uuid(track_in.album_id):
            return None
        album = self.db.query(Album).filter(Album.id == track_in.album_id).first()
        if not album:
            return None  # Will be handled by endpoint

        track = Track(
            name=track_in.name,
            date=track_in.date,
            album_id=track_in.album_id,
        )
        self.db.add(track)
        self.db.commit()
        self.db.refresh(track)
        return track

    def update_track(self, track_id: str, track_in: TrackUpdate) -> Optional[Track]:
        """Update a track."""
        if not is_valid_uuid(track_id):
            return None
        track = self.get_track(track_id)
        if not track:
            return None

        update_data = track_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(track, field, value)

        self.db.commit()
        self.db.refresh(track)
        return track

    def delete_track(self, track_id: str) -> bool:
        """Delete a track. Returns True if deleted, False if not found."""
        if not is_valid_uuid(track_id):
            return False
        track = self.get_track(track_id)
        if not track:
            return False

        self.db.delete(track)
        self.db.commit()
        return True