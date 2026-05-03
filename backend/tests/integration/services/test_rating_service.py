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
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        result = rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=5))

        assert result is not None
        rating_obj, avg_rating = result
        assert rating_obj.rating == 5
        assert avg_rating is not None

    def test_not_purchased(self, db_session, normal_user):
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        rating_s = RatingService(db_session)
        result = rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=5))

        assert result is None

    def test_invalid_rating(self, db_session, normal_user):
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        result = rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=10))
        assert result is None


class TestRatingServiceUpdateRating:
    def test_successful_update(self, db_session, normal_user):
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=3))

        result = rating_s.update_rating(str(normal_user.id), str(album.id), RatingUpdate(rating=5))
        assert result is not None
        rating_obj, avg_rating = result
        assert rating_obj.rating == 5


class TestRatingServiceGetUserRatings:
    def test_get_ratings(self, db_session, normal_user):
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=4))

        result, total = rating_s.get_user_ratings(str(normal_user.id))
        assert total >= 1
        rating_obj, album_name, avg_rating = result[0]
        assert album_name == "A"
        assert rating_obj.rating == 4

    def test_get_ratings_pagination(self, db_session, normal_user):
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="B", performing_name="B", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        rating_s = RatingService(db_session)
        for i in range(5):
            album = album_s.create_album(AlbumCreate(name=f"Album{i}", price=10.0, artist_id=str(artist.id), genre_ids=[]))
            purchase_s = PurchaseService(db_session)
            purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))
            rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=3))

        page1, total1 = rating_s.get_user_ratings(str(normal_user.id), page=1, page_size=3)
        assert len(page1) == 3
        page2, total2 = rating_s.get_user_ratings(str(normal_user.id), page=2, page_size=3)
        assert len(page2) == 2


class TestRatingServiceGetAlbumRatings:
    def test_get_album_ratings(self, db_session, normal_user):
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        rating_s = RatingService(db_session)
        rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=5))

        result = rating_s.get_album_ratings(str(album.id))
        assert result is not None
        rating_responses, avg_rating, total = result
        assert len(rating_responses) >= 1
        assert avg_rating is not None
        assert rating_responses[0].album_name == "A"
        assert rating_responses[0].user_rating == 5

    def test_get_album_ratings_pagination(self, db_session, normal_user):
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.services.purchase_service import PurchaseService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="C", performing_name="C", date_of_birth=date(2000, 1, 1)))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="C", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))
        rating_s = RatingService(db_session)
        rating_s.create_or_update_rating(str(normal_user.id), RatingCreate(album_id=str(album.id), rating=4))

        result = rating_s.get_album_ratings(str(album.id), page=1, page_size=0)
        assert result is not None
        rating_responses, avg_rating, total = result
        assert len(rating_responses) == 0

        result = rating_s.get_album_ratings(str(album.id), page=1, page_size=10)
        assert result is not None
        rating_responses, avg_rating, total = result
        assert len(rating_responses) == 1
        assert rating_responses[0].user_rating == 4
