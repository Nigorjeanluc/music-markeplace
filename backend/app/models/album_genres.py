from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class AlbumGenre(Base):
    __tablename__ = "album_genres"

    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(UUID(as_uuid=True), ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
