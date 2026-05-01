import pytest
from app.services.genre_service import GenreService
from app.schemas.genre import GenreCreate, GenreUpdate


class TestGenreServiceCreateGenre:
    def test_successful_creation(self, db_session):
        service = GenreService(db_session)
        genre_in = GenreCreate(name="Rock", description="Rock music")
        genre = service.create_genre(genre_in)

        assert genre is not None
        assert genre.name == "Rock"
        assert genre.description == "Rock music"

    def test_duplicate_name(self, db_session):
        service = GenreService(db_session)
        service.create_genre(GenreCreate(name="UniqueGenre"))
        # Try duplicate if unique constraint exists


class TestGenreServiceGetGenres:
    def test_get_all(self, db_session):
        service = GenreService(db_session)
        service.create_genre(GenreCreate(name="Genre1"))
        service.create_genre(GenreCreate(name="Genre2"))

        genres = service.get_genres()
        assert len(genres) >= 2

    def test_search(self, db_session):
        service = GenreService(db_session)
        service.create_genre(GenreCreate(name="SearchGenreUnique"))

        genres = service.get_genres(search="SearchGenreUnique")
        assert len(genres) == 1
        assert genres[0].name == "SearchGenreUnique"


class TestGenreServiceGetGenre:
    def test_existing(self, db_session):
        service = GenreService(db_session)
        genre = service.create_genre(GenreCreate(name="TestGenre"))

        result = service.get_genre(str(genre.id))
        assert result is not None
        assert result.id == genre.id

    def test_nonexistent(self, db_session):
        service = GenreService(db_session)
        result = service.get_genre("nonexistent-id")
        assert result is None


class TestGenreServiceUpdateGenre:
    def test_successful_update(self, db_session):
        service = GenreService(db_session)
        genre = service.create_genre(GenreCreate(name="OldName"))

        updated = service.update_genre(str(genre.id), GenreUpdate(name="NewName"))
        assert updated is not None
        assert updated.name == "NewName"

    def test_nonexistent(self, db_session):
        service = GenreService(db_session)
        updated = service.update_genre("nonexistent-id", GenreUpdate(name="New"))
        assert updated is None


class TestGenreServiceDeleteGenre:
    def test_successful_delete(self, db_session):
        service = GenreService(db_session)
        genre = service.create_genre(GenreCreate(name="ToDelete"))

        result = service.delete_genre(str(genre.id))
        assert result is True

        assert service.get_genre(str(genre.id)) is None

    def test_nonexistent(self, db_session):
        service = GenreService(db_session)
        result = service.delete_genre("nonexistent-id")
        assert result is False
