from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Date, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, column_property
import uuid
from datetime import datetime
from app.db.base import Base


class Album(Base):
    __tablename__ = "albums"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artist_id = Column(UUID(as_uuid=True), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, index=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    release_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    artist = relationship("Artist", back_populates="albums")
    purchases = relationship("Purchase", back_populates="album", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="album", cascade="all, delete-orphan")
    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")