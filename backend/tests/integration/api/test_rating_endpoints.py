import pytest
import time

from app.schemas.purchase import PurchaseCreate

DUMMY_UUID = "00000000-0000-0000-0000-000000000000"


class TestCreateOrUpdateRating:
    def test_authenticated(self, client, user_token, normal_user, db_session):
        # Create artist, album, purchase first with unique names
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService
        from app.schemas.artist import ArtistCreate
        from app.schemas.album import AlbumCreate
        from datetime import date
        suffix = str(int(time.time() * 1000))
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name=f"R{suffix}", performing_name=f"R{suffix}", date_of_birth=date(2000, 1, 1)))
        assert artist is not None, "Failed to create artist"
        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name=f"RatingAlbum{suffix}", price=10.0, artist_id=str(artist.id), genre_ids=[]))
        assert album is not None, "Failed to create album"
        purchase_service = PurchaseService(db_session)
        purchase_service.create_purchase(normal_user.id, PurchaseCreate(album_id=str(album.id)))

        response = client.post("/api/v1/ratings/", json={
            "album_id": str(album.id),
            "rating": 5
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_unauthenticated(self, client):
        response = client.post("/api/v1/ratings/", json={
            "album_id": DUMMY_UUID,
            "rating": 5
        })
        assert response.status_code == 401

    def test_invalid_rating(self, client, user_token, normal_user, db_session):
        # Create artist, album, purchase first with unique names
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService
        from app.schemas.artist import ArtistCreate
        from app.schemas.album import AlbumCreate
        from datetime import date
        suffix = str(int(time.time() * 1000))
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name=f"R2{suffix}", performing_name=f"R2{suffix}", date_of_birth=date(2000, 1, 1)))
        assert artist is not None, "Failed to create artist"
        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name=f"RatingAlbum2{suffix}", price=10.0, artist_id=str(artist.id), genre_ids=[]))
        assert album is not None, "Failed to create album"
        purchase_service = PurchaseService(db_session)
        purchase_service.create_purchase(normal_user.id, PurchaseCreate(album_id=str(album.id)))

        response = client.post("/api/v1/ratings/", json={
            "album_id": str(album.id),
            "rating": 10  # Out of range
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code in [400, 422]


class TestUpdateRating:
    def test_authenticated(self, client, user_token, normal_user, db_session):
        # Create artist, album, purchase, rating first with unique names
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService
        from app.services.rating_service import RatingService
        from app.schemas.artist import ArtistCreate
        from app.schemas.album import AlbumCreate
        from app.schemas.rating import RatingCreate, RatingUpdate
        from app.schemas.purchase import PurchaseCreate
        from datetime import date
        suffix = str(int(time.time() * 1000))
        artist_service = ArtistService(db_session)
        artist = artist_service.create_artist(ArtistCreate(real_name=f"R3{suffix}", performing_name=f"R3{suffix}", date_of_birth=date(2000, 1, 1)))
        assert artist is not None, "Failed to create artist"
        album_service = AlbumService(db_session)
        album = album_service.create_album(AlbumCreate(name=f"RatingAlbum3{suffix}", price=10.0, artist_id=str(artist.id), genre_ids=[]))
        assert album is not None, "Failed to create album"
        purchase_service = PurchaseService(db_session)
        purchase_service.create_purchase(normal_user.id, PurchaseCreate(album_id=str(album.id)))
        rating_service = RatingService(db_session)
        rating_service.create_or_update_rating(normal_user.id, RatingCreate(album_id=str(album.id), rating=3))

        response = client.put(f"/api/v1/ratings/{album.id}", json={
            "rating": 4
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_unauthenticated(self, client):
        response = client.put(f"/api/v1/ratings/{DUMMY_UUID}", json={"rating": 4})
        assert response.status_code == 401


class TestGetUserRatings:
    def test_authenticated(self, client, user_token):
        response = client.get("/api/v1/ratings/me", headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_unauthenticated(self, client):
        response = client.get("/api/v1/ratings/me")
        assert response.status_code == 401


class TestGetAlbumRatings:
    def test_public_access(self, client):
        response = client.get(f"/api/v1/ratings/album/{DUMMY_UUID}")
        assert response.status_code in [200, 404]
