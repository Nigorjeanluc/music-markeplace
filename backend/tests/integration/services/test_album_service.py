import pytest
from datetime import date
from app.services.album_service import AlbumService
from app.services.artist_service import ArtistService
from app.schemas.album import AlbumCreate, AlbumUpdate
from app.schemas.artist import ArtistCreate


class TestAlbumServiceCreateAlbum:
    def test_successful_creation(self, db_session):
        # Create artist first
        artist_service = ArtistService(db_session)
        from datetime import date
        artist_in = ArtistCreate(real_name="Test Artist", performing_name="TestPerforming", date_of_birth=date.today())
        artist = artist_service.create_artist(artist_in)

        # Create album
        album_service = AlbumService(db_session)
        album_in = AlbumCreate(
            name="Test Album",
            price=9.99,
            artist_id=str(artist.id),
            genre_ids=[]
        )
        album = album_service.create_album(album_in)

        assert album is not None
        assert album.name == "Test Album"
        assert float(album.price) == 9.99
        assert album.artist_id == artist.id

    def test_artist_not_found(self, db_session):
        album_service = AlbumService(db_session)
        album_in = AlbumCreate(
            name="Test Album",
            price=9.99,
            artist_id="00000000-0000-0000-0000-000000000000",
            genre_ids=[]
        )
        album = album_service.create_album(album_in)
        assert album is None


class TestAlbumServiceGetAlbums:
    def test_get_all_albums(self, db_session):
        # Create artist and album
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="Artist 1", performing_name="Artist 1", date_of_birth=date.today()))

        album_service = AlbumService(db_session)
        album_service.create_album(AlbumCreate(name="Album 1", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        albums = album_service.get_albums()
        assert len(albums) >= 1
        assert albums[0][0].name == "Album 1"  # First element is Album object

    def test_filter_by_artist(self, db_session):
        # Create two artists
        artist_service = ArtistService(db_session)
        artist1 = artist_service.create_artist(ArtistCreate(real_name="Artist 1", performing_name="Artist 1", date_of_birth=date.today()))
        artist2 = artist_service.create_artist(ArtistCreate(real_name="Artist 2", performing_name="Artist 2", date_of_birth=date.today()))

        album_service = AlbumService(db_session)
        album_service.create_album(AlbumCreate(name="Album 1", price=10.0, artist_id=str(artist1.id), genre_ids=[]))
        album_service.create_album(AlbumCreate(name="Album 2", price=12.0, artist_id=str(artist2.id), genre_ids=[]))

        albums = album_service.get_albums(artist_id=str(artist1.id))
        assert len(albums) == 1
        assert albums[0][0].artist_id == artist1.id


class TestAlbumServiceGetAlbum:
    def test_existing_album(self, db_session):
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="Test Artist", performing_name="Test Artist", date_of_birth=date.today()))

        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name="Test Album", price=9.99, artist_id=str(artist.id), genre_ids=[]))

        result = album_service.get_album(str(album.id))
        assert result is not None
        assert result[0].id == album.id  # First element is Album

    def test_nonexistent_album(self, db_session):
        album_service = AlbumService(db_session)
        result = album_service.get_album("nonexistent-id")
        assert result is None


class TestAlbumServiceUpdateAlbum:
    def test_successful_update(self, db_session):
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="Test Artist", performing_name="Test Artist", date_of_birth=date.today()))

        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name="Old Name", price=9.99, artist_id=str(artist.id), genre_ids=[]))

        updated = album_service.update_album(str(album.id), AlbumUpdate(name="New Name", price=12.99))
        assert updated is not None
        assert updated.name == "New Name"
        assert float(updated.price) == 12.99

    def test_nonexistent_album(self, db_session):
        album_service = AlbumService(db_session)
        updated = album_service.update_album("nonexistent-id", AlbumUpdate(name="New Name"))
        assert updated is None


class TestAlbumServiceDeleteAlbum:
    def test_successful_delete(self, db_session):
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="Test Artist", performing_name="Test Artist", date_of_birth=date.today()))

        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name="To Delete", price=9.99, artist_id=str(artist.id), genre_ids=[]))

        result = album_service.delete_album(str(album.id))
        assert result is True

        # Verify deleted
        assert album_service.get_album(str(album.id)) is None

    def test_nonexistent_album(self, db_session):
        album_service = AlbumService(db_session)
        result = album_service.delete_album("nonexistent-id")
        assert result is False
