from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate


class GenreService:
    def __init__(self, db: Session):
        self.db = db

    def get_genres(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Genre]:
        """Get genres with optional search."""
        query = self.db.query(Genre)
        if search:
            query = query.filter(Genre.name.ilike(f"%{search}%"))
        return query.order_by(Genre.name).offset(skip).limit(limit).all()

    def get_genre(self, genre_id: str) -> Optional[Genre]:
        """Get a genre by ID."""
        return self.db.query(Genre).filter(Genre.id == genre_id).first()

    def create_genre(self, genre_in: GenreCreate) -> Genre:
        """Create a new genre."""
        genre = Genre(
            name=genre_in.name,
            description=genre_in.description,
        )
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def update_genre(self, genre_id: str, genre_in: GenreUpdate) -> Optional[Genre]:
        """Update a genre."""
        genre = self.get_genre(genre_id)
        if not genre:
            return None

        update_data = genre_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(genre, field, value)

        self.db.commit()
        self.db.refresh(genre)
        return genre

    def delete_genre(self, genre_id: str) -> bool:
        """Delete a genre. Returns True if deleted, False if not found."""
        genre = self.get_genre(genre_id)
        if not genre:
            return False

        self.db.delete(genre)
        self.db.commit()
        return True
