from sqlalchemy.orm import Session
from typing import List, Optional, Tuple

from app.models.artist import Artist
from app.models.album import Album
from app.schemas.artist import ArtistCreate, ArtistUpdate


class ArtistService:
    def __init__(self, db: Session):
        self.db = db

    def get_artists(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Tuple[Artist, int]]:
        """Get artists with optional search, returning tuples of (artist, album_count)."""
        query = self.db.query(Artist)
        if search:
            query = query.filter(Artist.performing_name.ilike(f"%{search}%"))
        artists = query.offset(skip).limit(limit).all()

        # Add album_count to each artist
        result = []
        for artist in artists:
            album_count = self.db.query(Album).filter(Album.artist_id == artist.id).count()
            result.append((artist, album_count))
        return result

    def get_artist(self, artist_id: str) -> Optional[Tuple[Artist, int]]:
        """Get artist detail with album count, returning tuple of (artist, album_count)."""
        artist = self.db.query(Artist).filter(Artist.id == artist_id).first()
        if not artist:
            return None

        album_count = self.db.query(Album).filter(Album.artist_id == artist.id).count()
        return (artist, album_count)

    def create_artist(self, artist_in: ArtistCreate) -> Artist:
        """Create a new artist."""
        artist = Artist(
            real_name=artist_in.real_name,
            performing_name=artist_in.performing_name,
            date_of_birth=artist_in.date_of_birth,
        )
        self.db.add(artist)
        self.db.commit()
        self.db.refresh(artist)
        return artist

    def update_artist(self, artist_id: str, artist_in: ArtistUpdate) -> Optional[Artist]:
        """Update an artist."""
        artist = self.get_artist(artist_id)
        if not artist:
            return None

        artist_obj = artist[0]  # Extract artist from tuple

        update_data = artist_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(artist_obj, field, value)

        self.db.commit()
        self.db.refresh(artist_obj)
        return artist_obj

    def delete_artist(self, artist_id: str) -> bool:
        """Delete an artist. Returns True if deleted, False if not found."""
        artist = self.db.query(Artist).filter(Artist.id == artist_id).first()
        if not artist:
            return False

        self.db.delete(artist)
        self.db.commit()
        return True