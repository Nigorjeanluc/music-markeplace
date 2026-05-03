import pytest
from datetime import date
from app.services.purchase_service import PurchaseService
from app.schemas.purchase import PurchaseCreate
from app.schemas.album import AlbumCreate
from app.schemas.artist import ArtistCreate


class TestPurchaseServiceCreatePurchase:
    def test_successful_purchase(self, db_session, normal_user):
        # Create artist and album
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date.today()))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        # Purchase
        purchase_s = PurchaseService(db_session)
        purchase = purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        assert purchase is not None
        assert purchase.user_id == normal_user.id
        assert purchase.album_id == album.id
        assert float(purchase.amount_paid) == 10.0

    def test_duplicate_purchase(self, db_session, normal_user):
        # Create artist, album, purchase once, try again
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.schemas.album import AlbumCreate
        from app.schemas.artist import ArtistCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date.today()))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        # Duplicate
        duplicate = purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))
        assert duplicate is None

    def test_album_not_found(self, db_session, normal_user):
        purchase_s = PurchaseService(db_session)
        purchase = purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id="nonexistent"))
        assert purchase is None


class TestPurchaseServiceGetUserPurchases:
    def test_get_purchases(self, db_session, normal_user):
        # Create artist, album, purchase
        from app.services.artist_service import ArtistService
        from app.services.album_service import AlbumService
        from app.schemas.album import AlbumCreate
        from app.schemas.artist import ArtistCreate

        artist_s = ArtistService(db_session)
        artist = artist_s.create_artist(ArtistCreate(real_name="A", performing_name="A", date_of_birth=date.today()))

        album_s = AlbumService(db_session)
        album = album_s.create_album(AlbumCreate(name="A", price=10.0, artist_id=str(artist.id), genre_ids=[]))

        purchase_s = PurchaseService(db_session)
        purchase_s.create_purchase(str(normal_user.id), PurchaseCreate(album_id=str(album.id)))

        # Get purchases
        result, total = purchase_s.get_user_purchases(str(normal_user.id))
        assert total >= 1
        # Each element is (purchase, album, artist, user_rating, avg_rating)
        assert result[0][1] is not None  # album exists
