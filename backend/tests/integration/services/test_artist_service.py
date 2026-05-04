import pytest
from datetime import date
from app.services.artist_service import ArtistService
from app.schemas.artist import ArtistCreate, ArtistUpdate


class TestArtistServiceCreateArtist:
    def test_successful_creation(self, db_session):
        service = ArtistService(db_session)
        from datetime import date
        artist_in = ArtistCreate(real_name="John Doe", performing_name="JD", date_of_birth=date.today())
        artist = service.create_artist(artist_in)

        assert artist is not None
        assert artist.performing_name == "JD"
        assert artist.real_name == "John Doe"

    def test_duplicate_performing_name(self, db_session):
        service = ArtistService(db_session)
        service.create_artist(ArtistCreate(real_name="A", performing_name="UniqueName", date_of_birth=date.today()))
        # Try to create another with same performing name (if unique constraint exists)
        # This depends on model definition


class TestArtistServiceGetArtists:
    def test_get_all(self, db_session):
        service = ArtistService(db_session)
        service.create_artist(ArtistCreate(real_name="A1", performing_name="Artist1", date_of_birth=date.today()))
        service.create_artist(ArtistCreate(real_name="A2", performing_name="Artist2", date_of_birth=date.today()))

        result, total = service.get_artists()
        assert total >= 2
        # Each element is (artist, album_count)
        assert result[0][1] >= 0  # album_count is present

    def test_search(self, db_session):
        service = ArtistService(db_session)
        service.create_artist(ArtistCreate(real_name="Search Me", performing_name="SearchUnique", date_of_birth=date.today()))

        result, total = service.get_artists(search="SearchUnique")
        assert total == 1
        assert result[0][0].performing_name == "SearchUnique"


class TestArtistServiceGetArtist:
    def test_existing(self, db_session):
        service = ArtistService(db_session)
        artist = service.create_artist(ArtistCreate(real_name="Test", performing_name="TestArtist", date_of_birth=date.today()))

        result = service.get_artist(str(artist.id))
        assert result is not None
        assert result[0].id == artist.id

    def test_nonexistent(self, db_session):
        service = ArtistService(db_session)
        result = service.get_artist("nonexistent-id")
        assert result is None


class TestArtistServiceUpdateArtist:
    def test_successful_update(self, db_session):
        service = ArtistService(db_session)
        artist = service.create_artist(ArtistCreate(real_name="Old", performing_name="OldName", date_of_birth=date.today()))

        updated = service.update_artist(str(artist.id), ArtistUpdate(performing_name="NewName"))
        assert updated is not None
        assert updated.performing_name == "NewName"

    def test_nonexistent(self, db_session):
        service = ArtistService(db_session)
        updated = service.update_artist("nonexistent-id", ArtistUpdate(performing_name="New"))
        assert updated is None


class TestArtistServiceDeleteArtist:
    def test_successful_delete(self, db_session):
        service = ArtistService(db_session)
        artist = service.create_artist(ArtistCreate(real_name="ToDelete", performing_name="DelArtist", date_of_birth=date.today()))

        result = service.delete_artist(str(artist.id))
        assert result is True

        assert service.get_artist(str(artist.id)) is None

    def test_nonexistent(self, db_session):
        service = ArtistService(db_session)
        result = service.delete_artist("nonexistent-id")
        assert result is False
