import pytest
import time

DUMMY_UUID = "00000000-0000-0000-0000-000000000000"


class TestListTracks:
    def test_public_access(self, client):
        response = client.get("/api/v1/tracks/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_filter_by_album(self, client):
        response = client.get(f"/api/v1/tracks/?album_id={DUMMY_UUID}")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data


class TestGetTrack:
    def test_public_access(self, client):
        response = client.get(f"/api/v1/tracks/{DUMMY_UUID}")
        assert response.status_code == 404


class TestCreateTrack:
    def test_admin_only(self, client, admin_token, db_session):
        # Create artist and album first with unique names
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.schemas.artist import ArtistCreate
        from app.schemas.album import AlbumCreate
        from datetime import date
        suffix = str(int(time.time() * 1000))
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name=f"T{suffix}", performing_name=f"T{suffix}", date_of_birth=date(2000, 1, 1)))
        assert artist is not None, "Failed to create artist"
        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name=f"TrackAlbum{suffix}", price=10.0, artist_id=str(artist.id), genre_ids=[]))
        assert album is not None, "Failed to create album"

        response = client.post("/api/v1/tracks/", json={
            "name": "New Track",
            "date": "2023-01-01",
            "album_id": str(album.id)
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200

    def test_unauthorized(self, client):
        response = client.post("/api/v1/tracks/", json={
            "name": "New Track",
            "album_id": DUMMY_UUID
        })
        assert response.status_code == 401


class TestUpdateTrack:
    def test_admin_only(self, client, admin_token):
        response = client.put(f"/api/v1/tracks/{DUMMY_UUID}", json={
            "name": "Updated"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404

    def test_unauthorized(self, client):
        response = client.put(f"/api/v1/tracks/{DUMMY_UUID}", json={"name": "Updated"})
        assert response.status_code == 401


class TestDeleteTrack:
    def test_admin_only(self, client, admin_token):
        response = client.delete(f"/api/v1/tracks/{DUMMY_UUID}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 404

    def test_unauthorized(self, client):
        response = client.delete(f"/api/v1/tracks/{DUMMY_UUID}")
        assert response.status_code == 401
