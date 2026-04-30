from sqlalchemy import Column, DateTime, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id", ondelete="CASCADE"), nullable=False)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    amount_paid = Column(Numeric(10, 2), nullable=False)

    # Relationships
    user = relationship("User", back_populates="purchases")
    album = relationship("Album", back_populates="purchases")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'album_id', name='unique_user_album_purchase'),
    )