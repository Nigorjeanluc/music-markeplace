from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define the relationship with the PlaylistTrack model
    playlist_tracks = relationship("PlaylistTrack", back_populates="playlist")