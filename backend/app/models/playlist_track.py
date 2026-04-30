from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base


class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    playlist_id = Column(UUID(as_uuid=True), ForeignKey("playlists.id", ondelete="CASCADE"), nullable=False)
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define the relationships with the Playlist and Track models
    playlist = relationship("Playlist", back_populates="playlist_tracks")
    track = relationship("Track", back_populates="playlist_tracks")