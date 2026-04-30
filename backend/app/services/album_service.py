from sqlalchemy.orm import Session
from sqlalchemy import func, text, select
from typing import List, Optional, Tuple

from app.models.album import Album
from app.models.artist import Artist
from app.models.rating import Rating
from app.models.purchase import Purchase
from app.models.album_genres import AlbumGenre
from app.models.genre import Genre
from app.schemas.album import AlbumCreate, AlbumUpdate


class AlbumService:
    def __init__(self, db: Session):
        self.db = db

    def _get_album_rating_subquery(self):
        """Subquery to compute average rating from purchasers only."""
        return (
            select(func.avg(Rating.rating))
            .join(Purchase, (Rating.user_id == Purchase.user_id) & (Rating.album_id == Purchase.album_id))
            .where(Rating.album_id == Album.id)
            .correlate(Album)
            .scalar_subquery()
        )

    def get_albums(
        self,
        skip: int = 0,
        limit: int = 100,
        artist_id: Optional[str] = None,
        genre: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Tuple[Album, Optional[float], List[str], Optional[Artist]]]:
        """Get albums with filters, returning tuples of (album, avg_rating, genre_names, artist)."""
        query = self.db.query(Album)
        if artist_id:
            query = query.filter(Album.artist_id == artist_id)
        if search:
            query = query.filter(Album.name.ilike(f"%{search}%"))
        if genre:
            query = query.join(AlbumGenre, AlbumGenre.album_id == Album.id).join(Genre, Genre.id == AlbumGenre.genre_id).filter(Genre.name == genre)

        albums = query.offset(skip).limit(limit).all()

        # Compute rating and genre names for each album
        rating_subq = self._get_album_rating_subquery()
        result = []
        for album in albums:
            avg_rating = self.db.query(rating_subq).filter(Album.id == album.id).scalar()

            # Get genre names
            genre_names = [
                g.name for g in
                self.db.query(Genre).join(AlbumGenre, AlbumGenre.genre_id == Genre.id).filter(AlbumGenre.album_id == album.id).all()
            ]

            # Get artist
            artist = self.db.query(Artist).filter(Artist.id == album.artist_id).first()

            result.append((album, avg_rating, genre_names, artist))
        return result

    def get_album(self, album_id: str) -> Optional[Tuple[Album, Optional[float], List[str], Optional[Artist]]]:
        """Get album detail with rating, returning tuple of (album, avg_rating, genre_names, artist)."""
        album = self.db.query(Album).filter(Album.id == album_id).first()
        if not album:
            return None

        # Compute average rating
        rating_subq = self._get_album_rating_subquery()
        avg_rating = self.db.query(rating_subq).filter(Album.id == album_id).scalar()

        # Get genre names
        genre_names = [
            g.name for g in
            self.db.query(Genre).join(AlbumGenre, AlbumGenre.genre_id == Genre.id).filter(AlbumGenre.album_id == album_id).all()
        ]

        # Get artist
        artist = self.db.query(Artist).filter(Artist.id == album.artist_id).first()

        return (album, avg_rating, genre_names, artist)

    def create_album(self, album_in: AlbumCreate) -> Optional[Album]:
        """Create a new album."""
        # Verify artist exists
        artist = self.db.query(Artist).filter(Artist.id == album_in.artist_id).first()
        if not artist:
            return None

        album = Album(
            name=album_in.name,
            price=album_in.price,
            release_date=album_in.release_date,
            artist_id=album_in.artist_id,
        )
        self.db.add(album)
        self.db.flush()  # Get album.id

        # Add genre associations
        for genre_id in album_in.genre_ids:
            album_genre = AlbumGenre(album_id=album.id, genre_id=genre_id)
            self.db.add(album_genre)

        self.db.commit()
        self.db.refresh(album)
        return album

    def update_album(self, album_id: str, album_in: AlbumUpdate) -> Optional[Album]:
        """Update an album."""
        album = self.db.query(Album).filter(Album.id == album_id).first()
        if not album:
            return None

        update_data = album_in.model_dump(exclude_unset=True)
        genre_ids = update_data.pop("genre_ids", None)

        for field, value in update_data.items():
            setattr(album, field, value)

        # Update genre associations if provided
        if genre_ids is not None:
            # Remove old associations
            self.db.query(AlbumGenre).filter(AlbumGenre.album_id == album.id).delete()
            # Add new associations
            for genre_id in genre_ids:
                album_genre = AlbumGenre(album_id=album.id, genre_id=genre_id)
                self.db.add(album_genre)

        self.db.commit()
        self.db.refresh(album)
        return album

    def delete_album(self, album_id: str) -> bool:
        """Delete an album. Returns True if deleted, False if not found."""
        album = self.db.query(Album).filter(Album.id == album_id).first()
        if not album:
            return False

        self.db.delete(album)
        self.db.commit()
        return True