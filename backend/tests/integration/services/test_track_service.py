import pytest
from datetime import date
from app.services.track_service import TrackService
from app.services.album_service import AlbumService
from app.services.artist_service import ArtistService
from app.schemas.track import TrackCreate, TrackUpdate
from app.schemas.album import AlbumCreate
from app.schemas.artist import ArtistCreate


class TestTrackServiceCreateTrack:
    def test_successful_creation(self, db_session):
        # Create artist and album first
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name="Album", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        # Create track
        track_service = TrackService(db_session)
        track_in = TrackCreate(name="Track 1", date=date(2023, 1, 1), album_id=str(album.id))
        track = track_service.create_track(track_in)

        assert track is not None
        assert track.name == "Track 1"
        assert track.album_id == album.id

    def test_album_not_found(self, db_session):
        track_service = TrackService(db_session)
        track_in = TrackCreate(name="Track 1", date=date(2023, 1, 1), album_id="nonexistent-id")
        track = track_service.create_track(track_in)
        assert track is None


class TestTrackServiceGetTracks:
    def test_get_all(self, db_session):
        # Create artist, album, track
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name="Album", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        track_service = TrackService(db_session)
        track_service.create_track(TrackCreate(name="Track1", date=date(2023, 1, 1), album_id=str(album.id)))

        tracks = track_service.get_tracks()
        assert len(tracks) >= 1

    def test_filter_by_album(self, db_session):
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_service = AlbumService(db_session)
        album1 = album_service.create_album(AlbumCreate(name="Album1", price=10.0, artist_id=str(artist.id), genre_ids=[]))
        album2 = album_service.create_album(AlbumCreate(name="Album2", price=12.0, artist_id=str(artist.id), genre_ids=[]))

        track_service = TrackService(db_session)
        track_service.create_track(TrackCreate(name="T1", date=date(2023, 1, 1), album_id=str(album1.id)))
        track_service.create_track(TrackCreate(name="T2", date=date(2023, 1, 2), album_id=str(album2.id)))

        tracks = track_service.get_tracks(album_id=str(album1.id))
        assert len(tracks) == 1
        assert tracks[0].album_id == album1.id


class TestTrackServiceGetTrack:
    def test_existing(self, db_session):
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name="Album", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        track_service = TrackService(db_session)
        track = track_service.create_track(TrackCreate(name="Track", date=date(2023, 1, 1), album_id=str(album.id)))

        result = track_service.get_track(str(track.id))
        assert result is not None
        assert result.id == track.id

    def test_nonexistent(self, db_session):
        track_service = TrackService(db_session)
        result = track_service.get_track("nonexistent-id")
        assert result is None


class TestTrackServiceUpdateTrack:
    def test_successful_update(self, db_session):
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name="Album", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        track_service = TrackService(db_session)
        track = track_service.create_track(TrackCreate(name="Old", date=date(2023, 1, 1), album_id=str(album.id)))

        updated = track_service.update_track(str(track.id), TrackUpdate(name="New"))
        assert updated is not None
        assert updated.name == "New"

    def test_nonexistent(self, db_session):
        track_service = TrackService(db_session)
        updated = track_service.update_track("nonexistent-id", TrackUpdate(name="New"))
        assert updated is None


class TestTrackServiceDeleteTrack:
    def test_successful_delete(self, db_session):
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name="Album", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        track_service = TrackService(db_session)
        track = track_service.create_track(TrackCreate(name="ToDelete", date=date(2023, 1, 1), album_id=str(album.id)))

        result = track_service.delete_track(str(track.id))
        assert result is True

        assert track_service.get_track(str(track.id)) is None

    def test_nonexistent(self, db_session):
        track_service = TrackService(db_session)
        result = track_service.delete_track("nonexistent-id")
        assert result is False
