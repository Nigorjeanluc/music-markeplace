import pytest
import time

DUMMY_UUID = "00000000-0000-0000-0000-000000000000"


class TestCreatePurchase:
    def test_authenticated(self, client, user_token, normal_user, db_session):
        # Create artist, album first with unique names
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.schemas.artist import ArtistCreate
        from app.schemas.album import AlbumCreate
        from datetime import date
        suffix = str(int(time.time() * 1000))
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name=f"P{suffix}", performing_name=f"P{suffix}", date_of_birth=date(2000, 1, 1)))
        assert artist is not None, "Failed to create artist"
        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name=f"Album{suffix}", price=10.0, artist_id=str(artist.id), genre_ids=[]))
        assert album is not None, "Failed to create album"

        response = client.post("/api/v1/purchases/", json={
            "album_id": str(album.id)
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_unauthenticated(self, client):
        response = client.post("/api/v1/purchases/", json={
            "album_id": DUMMY_UUID
        })
        assert response.status_code == 401


class TestGetUserPurchases:
    def test_authenticated(self, client, user_token):
        response = client.get("/api/v1/purchases/me/library", headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_unauthenticated(self, client):
        response = client.get("/api/v1/purchases/me/library")
        assert response.status_code == 401
