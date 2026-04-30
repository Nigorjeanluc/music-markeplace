from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="ratings")
    album = relationship("Album", back_populates="ratings")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'album_id', name='unique_user_album_rating'),
        CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating_range'),
    )