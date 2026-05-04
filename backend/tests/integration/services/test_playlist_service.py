import pytest
from datetime import date
from app.services.playlist_service import PlaylistService
from app.services.auth_service import AuthService
from app.schemas.playlist import PlaylistCreate, PlaylistUpdate
from app.schemas.user import UserCreate
from app.schemas.artist import ArtistCreate


class TestPlaylistServiceCreatePlaylist:
    def test_successful_creation(self, db_session, normal_user):
        service = PlaylistService(db_session)
        playlist_in = PlaylistCreate(name="My Playlist", track_ids=[])
        playlist = service.create_playlist(playlist_in, user_id=str(normal_user.id))

        assert playlist is not None
        assert playlist.name == "My Playlist"
        assert playlist.user_id == normal_user.id

    def test_with_tracks(self, db_session, normal_user):
        # Create artist, album, track first
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.track_service import TrackService
        from app.schemas.album import AlbumCreate
        from app.schemas.track import TrackCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date.today()))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        track_s = TrackService(db_session)
        track = track_s.create_track(TrackCreate(name="T", date=date(2023, 1, 1), album_id=str(album.id)))

        # Create playlist with track
        service = PlaylistService(db_session)
        playlist_in = PlaylistCreate(name="With Tracks", track_ids=[str(track.id)])
        playlist = service.create_playlist(playlist_in, user_id=str(normal_user.id))

        assert playlist is not None
        # Check track count
        assert service.get_playlist_track_count(playlist.id) == 1


class TestPlaylistServiceGetPlaylists:
    def test_get_user_playlists(self, db_session, normal_user):
        service = PlaylistService(db_session)
        service.create_playlist(PlaylistCreate(name="P1"), user_id=str(normal_user.id))
        service.create_playlist(PlaylistCreate(name="P2"), user_id=str(normal_user.id))

        playlists = service.get_playlists(user_id=str(normal_user.id))
        assert len(playlists) >= 2


class TestPlaylistServiceGetPlaylist:
    def test_existing(self, db_session, normal_user):
        service = PlaylistService(db_session)
        playlist = service.create_playlist(PlaylistCreate(name="Test"), user_id=str(normal_user.id))

        result = service.get_playlist(str(playlist.id), user_id=str(normal_user.id))
        assert result is not None
        assert result.id == playlist.id

    def test_other_user_playlist(self, db_session, normal_user, admin_user):
        service = PlaylistService(db_session)
        # Admin creates playlist
        admin_playlist = service.create_playlist(PlaylistCreate(name="AdminP"), user_id=str(admin_user.id))
        # Normal user tries to access
        result = service.get_playlist(str(admin_playlist.id), user_id=str(normal_user.id))
        assert result is None


class TestPlaylistServiceUpdatePlaylist:
    def test_successful_update(self, db_session, normal_user):
        service = PlaylistService(db_session)
        playlist = service.create_playlist(PlaylistCreate(name="Old"), user_id=str(normal_user.id))

        updated = service.update_playlist(str(playlist.id), PlaylistUpdate(name="New"), user_id=str(normal_user.id))
        assert updated is not None
        assert updated.name == "New"

    def test_other_user(self, db_session, normal_user, admin_user):
        service = PlaylistService(db_session)
        admin_playlist = service.create_playlist(PlaylistCreate(name="AdminP"), user_id=str(admin_user.id))

        updated = service.update_playlist(str(admin_playlist.id), PlaylistUpdate(name="Hacked"), user_id=str(normal_user.id))
        assert updated is None


class TestPlaylistServiceDeletePlaylist:
    def test_successful_delete(self, db_session, normal_user):
        service = PlaylistService(db_session)
        playlist = service.create_playlist(PlaylistCreate(name="ToDelete"), user_id=str(normal_user.id))

        result = service.delete_playlist(str(playlist.id), user_id=str(normal_user.id))
        assert result is True

        assert service.get_playlist(str(playlist.id), user_id=str(normal_user.id)) is None

    def test_other_user(self, db_session, normal_user, admin_user):
        service = PlaylistService(db_session)
        admin_playlist = service.create_playlist(PlaylistCreate(name="AdminP"), user_id=str(admin_user.id))

        result = service.delete_playlist(str(admin_playlist.id), user_id=str(normal_user.id))
        assert result is False


class TestPlaylistServiceAddRemoveTracks:
    def test_add_track(self, db_session, normal_user):
        # Create track first
        from app.services.track_service import TrackService
        from app.services.album_service import AlbumService
        from app.services.artist_service import ArtistService
        from app.schemas.album import AlbumCreate
        from app.schemas.track import TrackCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date.today()))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        track_s = TrackService(db_session)
        track = track_s.create_track(TrackCreate(name="T", date=date(2023, 1, 1), album_id=str(album.id)))

        # Create playlist
        service = PlaylistService(db_session)
        playlist = service.create_playlist(PlaylistCreate(name="P"), user_id=str(normal_user.id))

        # Add track
        result = service.add_track_to_playlist(str(playlist.id), str(track.id), user_id=str(normal_user.id))
        assert result is True

        # Check track count
        assert service.get_playlist_track_count(str(playlist.id)) == 1

    def test_remove_track(self, db_session, normal_user):
        # Similar setup as above, add track then remove
        from app.services.track_service import TrackService
        from app.services.album_service import AlbumService
        from app.services.artist_service import ArtistService
        from app.schemas.album import AlbumCreate
        from app.schemas.track import TrackCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date.today()))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        track_s = TrackService(db_session)
        track = track_s.create_track(TrackCreate(name="T", date=date(2023, 1, 1), album_id=str(album.id)))

        service = PlaylistService(db_session)
        playlist = service.create_playlist(PlaylistCreate(name="P", track_ids=[str(track.id)]), user_id=str(normal_user.id))

        # Remove track
        result = service.remove_track_from_playlist(str(playlist.id), str(track.id), user_id=str(normal_user.id))
        assert result is True

        assert service.get_playlist_track_count(str(playlist.id)) == 0
