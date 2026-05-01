import pytest
from datetime import date
from app.services.rating_service import RatingService
from app.services.purchase_service import PurchaseService
from app.schemas.rating import RatingCreate, RatingUpdate
from app.schemas.purchase import PurchaseCreate
from app.schemas.album import AlbumCreate
from app.schemas.artist import ArtistCreate


class TestRatingServiceCreateOrUpdateRating:
    def test_successful_rating(self, db_session, normal_user):
        # Create artist, album, purchase first
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        # Purchase album
        purchase_s = PurchaseService(db_session)
        purchase = purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        # Rate album
        rating_s = RatingService(db_session)
        result = rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=5))

        assert result is not None
        rating_obj, avg_rating = result
        assert rating_obj.rating == 5
        assert avg_rating is not None

    def test_not_purchased(self, db_session, normal_user):
        # Create album but don't purchase
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.schemas.album import AlbumCreate
        from app.schemas.artist import ArtistCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        rating_s = RatingService(db_session)
        result = rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=5))

        assert result is None

    def test_invalid_rating(self, db_session, normal_user):
        # Create artist, album, purchase
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService
        from app.schemas.album import AlbumCreate
        from app.schemas.artist import ArtistCreate
        from app.schemas.purchase import PurchaseCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        # Rating out of range
        result = rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=10))
        assert result is None


class TestRatingServiceUpdateRating:
    def test_successful_update(self, db_session, normal_user):
        # Setup: create, purchase, rate
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService
        from app.schemas.album import AlbumCreate
        from app.schemas.artist import ArtistCreate
        from app.schemas.purchase import PurchaseCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=3))

        # Update
        result = rating_s.update_rating(str(normal_user.id), str(album.id), RatingUpdate(rating=5))
        assert result is not None
        rating_obj, avg_rating = result
        assert rating_obj.rating == 5


class TestRatingServiceGetUserRatings:
    def test_get_ratings(self, db_session, normal_user):
        # Setup: create, purchase, rate
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService
        from app.schemas.album import AlbumCreate
        from app.schemas.artist import ArtistCreate
        from app.schemas.purchase import PurchaseCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=4))

        # Get ratings
        ratings = rating_s.get_user_ratings(str(normal_user.id))
        assert len(ratings) >= 1


class TestRatingServiceGetAlbumRatings:
    def test_get_album_ratings(self, db_session, normal_user):
        # Setup: create, purchase, rate
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService
        from app.schemas.album import AlbumCreate
        from app.schemas.artist import ArtistCreate
        from app.schemas.purchase import PurchaseCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=5))

        # Get album ratings
        result = rating_s.get_album_ratings(str(album.id))
        assert result is not None
        ratings, album_obj, avg_rating = result
        assert len(ratings) >= 1
        assert avg_rating is not None
