"""
Database seed script for Music Marketplace.
Populates all tables with realistic data. Safe to run multiple times (idempotent).
"""
from datetime import date, datetime
import uuid

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.artist import Artist
from app.models.genre import Genre
from app.models.album import Album
from app.models.album_genres import AlbumGenre
from app.models.track import Track
from app.models.playlist import Playlist
from app.models.playlist_track import PlaylistTrack
from app.models.purchase import Purchase
from app.models.rating import Rating


# Fixed valid UUIDs for idempotency
ADMIN_ID = "d2a35645-2d87-487c-bf7a-304298355b43"
USER1_ID = "578c7f99-4e51-4d91-adf0-c61b2a92089c"
USER2_ID = "2997e4c4-8ce0-40fc-abbd-ca47f8c9f3f7"

ARTIST1_ID = "6a95c045-003f-4c92-bad9-b4b967f36d27"  # John Coltrane
ARTIST2_ID = "51eb38ee-42b0-4af3-b443-cb47cc73ebdd"  # Miles Davis
ARTIST3_ID = "ad344b59-be51-46a8-865e-b812f83ec8cd"  # Pink Floyd
ARTIST4_ID = "9187b1a0-6911-4bc8-a547-0b2e374a17a3"  # Radiohead
ARTIST5_ID = "89ba2356-f4df-4112-8b67-d3c9f7781cb8"  # James Brown
ARTIST6_ID = "687863c6-eb89-4178-8d90-b7db89d93387"  # Daft Punk
ARTIST7_ID = "f47ac10b-58cc-4372-a567-0e02b2c3d479"  # Saleheen Artist
ARTIST8_ID = "7c9e3b6a-1d2f-4a8c-b123-5f6e8c9d0e1a"  # Vishnu Artist

GENRE1_ID = "66d3b254-5979-494e-a702-417dcb1c3dee"  # Jazz
GENRE2_ID = "0cf468a2-e9e7-4ab8-a312-95fca026ff45"  # Rock
GENRE3_ID = "6ae05b8a-1eba-4cb7-985c-004a8c58b703"  # Classical
GENRE4_ID = "957d889e-b477-47bd-a192-5be3d4517864"  # Hip Hop
GENRE5_ID = "36ec104d-5eed-4098-8f3d-4b6ce9063dc1"  # Blues
GENRE6_ID = "ef0cadf5-1273-4e35-bb42-37b972f2c25c"  # Electronic
GENRE7_ID = "cb2423ea-8308-446c-9950-46b397e87764"  # Pop
GENRE8_ID = "9eb61390-0b45-402b-9105-6c3f23b099c5"  # R&B

ALBUM1_ID = "c189e851-6a3a-4493-9ec3-b2f66a5e0087"  # A Love Supreme
ALBUM2_ID = "89e069b6-574d-425a-966e-83b833c92038"  # Kind of Blue
ALBUM3_ID = "b77e0210-e6bb-4da3-9f56-df6643f4ff9a"  # The Dark Side of the Moon
ALBUM4_ID = "ee7f3c79-6047-48ca-9244-b27a4b8652a0"  # OK Computer
ALBUM5_ID = "a3a9a218-161c-4afb-916c-fdf92507a497"  # Kid A
ALBUM6_ID = "8bcd0ecc-dbb5-4505-9d82-7171ce2b261f"  # Live at the Apollo
ALBUM7_ID = "142069b2-c811-49cd-b42c-1273e1f1fee5"  # Random Access Memories
ALBUM8_ID = "14dcdb66-7001-413d-a220-ecbb6e8c7912"  # Discovery

TRACK1_ID = "633879a1-f7ff-4e62-ba53-1c8b43608044"  # Acknowledgement
TRACK2_ID = "59df3a16-3d6c-48b1-a24a-edc0b09f8da5"  # Resolution
TRACK3_ID = "289dbe37-1a54-462e-ac28-e34edb2f5d80"  # Pursuance
TRACK4_ID = "f150a412-086b-4053-8101-d7ac8f46ef91"  # So What
TRACK5_ID = "34d117c3-d419-4ad4-9375-39b7b64d3e38"  # All Blues
TRACK6_ID = "19b18128-afbe-470a-b0d4-4a72a14f8e07"  # Speak to Me
TRACK7_ID = "d99d4ec6-9aa1-4cf4-b087-4807913832c9"  # Breathe
TRACK8_ID = "4d8963ef-4a3e-4a16-87a3-2a08f0d82cb2"  # Time
TRACK9_ID = "a81b94ea-47c4-4ca4-a7ef-706c0838848e"  # Airbag
TRACK10_ID = "a36dd1f6-d49d-4f6b-9e26-039bcd65950d"  # Paranoid Android
TRACK11_ID = "6c8a3515-a9af-4a9c-97c1-0603b0d5b8fe"  # Everything in Its Right Place
TRACK12_ID = "2f55d5e7-18d5-49cc-89c1-e05a2a1bb00d"  # Kid A
TRACK13_ID = "543498a0-fd73-4a98-8611-c0d05285b8d4"  # Get Lucky
TRACK14_ID = "5cc1935a-3599-462c-aa26-f1d5d85ddaee"  # Lose Yourself to Dance
TRACK15_ID = "abc091d9-7f6c-4b84-8c83-d1949c55d3d6"  # One More Time
TRACK16_ID = "bdd47689-c531-4470-8949-3d54c3664474"  # Digital Love

PLAYLIST1_ID = "36da1690-5b31-4bae-84b6-0a4f95e0937e"  # My Jazz Collection
PLAYLIST2_ID = "5bddb238-abf2-4edf-8652-a5e93859b75f"  # Electronic Vibes
PLAYLIST3_ID = "6a0b7709-38e0-484f-aea8-f398c64b5b16"  # Rock Classics

PTRACK1_ID = "f5e2be84-6820-485d-82a9-b81891ebb042"
PTRACK2_ID = "e83cb368-2b2a-4bc6-ac34-0d8bd6fdfb0b"
PTRACK3_ID = "11909430-309e-480f-ab6e-51c0404e83e5"
PTRACK4_ID = "dcf49941-fba7-40e2-be13-da2efab5efbd"
PTRACK5_ID = "d1d1fca7-5609-4286-b5ad-e2b454d167a5"
PTRACK6_ID = "b7530a5d-ab75-4597-8717-1bc4602f230c"
PTRACK7_ID = "75b91422-0b47-4d8e-8a70-2720e10142f5"
PTRACK8_ID = "caf2170c-5321-4b28-b876-e0759634bdff"

PURCHASE1_ID = "b5b3b388-5545-4671-93f4-5f3e6136d072"
PURCHASE2_ID = "b07d1825-aceb-4f91-a938-f26eb63ecc66"
PURCHASE3_ID = "ed771370-32c5-46d5-928b-a0f16e9eed66"
PURCHASE4_ID = "54c5ddea-b0f5-4b45-b6a0-4726813c757c"
PURCHASE5_ID = "c29c2c43-e8e3-492c-8c00-024987b9b1be"
PURCHASE6_ID = "6d0aa5b0-4cc3-4cf6-ace5-32b623140fe5"

RATING1_ID = "7cf68b12-5602-4f6e-b29c-77d3a720b7a4"
RATING2_ID = "0f9f6939-57f8-48f4-a985-bd457b47756f"
RATING3_ID = "a65d3a37-2a49-4dfb-b5d2-1083ddba3ac9"
RATING4_ID = "af4af4fd-7b5b-4c26-ba8d-db69a419ee0e"
RATING5_ID = "73821fd7-0e4a-465d-941d-15c03bc73900"
RATING6_ID = "6ee05449-1c84-4e68-ada3-db4194805935"


def seed_data():
    """Seed all tables with realistic data. Idempotent."""
    db = SessionLocal()
    try:
        # Check if data already seeded
        if db.query(User).count() > 0:
            print("Data already exists. Skipping seed.")
            return

        print("Seeding database...")

        # 1. USERS
        print("  Creating users...")
        admin = User(
            id=uuid.UUID(ADMIN_ID),
            email="admin@musicmarket.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True,
            created_at=datetime(2025, 1, 1, 10, 0, 0),
            updated_at=datetime(2025, 1, 1, 10, 0, 0),
        )
        user1 = User(
            id=uuid.UUID(USER1_ID),
            email="john@musicmarket.com",
            username="john_doe",
            hashed_password=get_password_hash("password123"),
            is_admin=False,
            is_active=True,
            created_at=datetime(2025, 1, 2, 10, 0, 0),
            updated_at=datetime(2025, 1, 2, 10, 0, 0),
        )
        user2 = User(
            id=uuid.UUID(USER2_ID),
            email="jane@musicmarket.com",
            username="jane_smith",
            hashed_password=get_password_hash("password123"),
            is_admin=False,
            is_active=True,
            created_at=datetime(2025, 1, 3, 10, 0, 0),
            updated_at=datetime(2025, 1, 3, 10, 0, 0),
        )
        db.add_all([admin, user1, user2])
        db.flush()
        print(f"    Created 3 users")

        # 2. ARTISTS
        print("  Creating artists...")
        artists = [
            Artist(
                id=uuid.UUID(ARTIST1_ID),
                real_name="John Coltrane",
                performing_name="John Coltrane",
                date_of_birth=date(1926, 9, 23),
                photo_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/artists/aiden-marples-Udu9NgiNFk8-unsplash.jpg",
                created_at=datetime(2025, 1, 10, 10, 0, 0),
                updated_at=datetime(2025, 1, 10, 10, 0, 0),
            ),
            Artist(
                id=uuid.UUID(ARTIST2_ID),
                real_name="Miles Davis",
                performing_name="Miles Davis",
                date_of_birth=date(1926, 5, 26),
                photo_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/artists/darktopia-nWjT3nbHhso-unsplash.jpg",
                created_at=datetime(2025, 1, 10, 11, 0, 0),
                updated_at=datetime(2025, 1, 10, 11, 0, 0),
            ),
            Artist(
                id=uuid.UUID(ARTIST3_ID),
                real_name="Pink Floyd",
                performing_name="Pink Floyd",
                date_of_birth=date(1965, 1, 1),
                photo_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/artists/renee-thompson-VdN2CGmvM88-unsplash.jpg",
                created_at=datetime(2025, 1, 10, 12, 0, 0),
                updated_at=datetime(2025, 1, 10, 12, 0, 0),
            ),
            Artist(
                id=uuid.UUID(ARTIST4_ID),
                real_name="Thom Yorke",
                performing_name="Radiohead",
                date_of_birth=date(1968, 10, 7),
                photo_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/artists/tamara-gore-gr-0oDn91cE-unsplash.jpg",
                created_at=datetime(2025, 1, 10, 13, 0, 0),
                updated_at=datetime(2025, 1, 10, 13, 0, 0),
            ),
            Artist(
                id=uuid.UUID(ARTIST5_ID),
                real_name="James Brown",
                performing_name="James Brown",
                date_of_birth=date(1933, 5, 3),
                photo_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/artists/aiden-marples-Udu9NgiNFk8-unsplash.jpg",
                created_at=datetime(2025, 1, 10, 14, 0, 0),
                updated_at=datetime(2025, 1, 10, 14, 0, 0),
            ),
            Artist(
                id=uuid.UUID(ARTIST6_ID),
                real_name="Daft Punk",
                performing_name="Daft Punk",
                date_of_birth=date(1993, 1, 1),
                photo_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/artists/darktopia-nWjT3nbHhso-unsplash.jpg",
                created_at=datetime(2025, 1, 10, 15, 0, 0),
                updated_at=datetime(2025, 1, 10, 15, 0, 0),
            ),
            Artist(
                id=uuid.UUID(ARTIST7_ID),
                real_name="Saleheen Muhammad Mustak",
                performing_name="Saleheen",
                date_of_birth=date(1990, 1, 1),
                photo_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/artists/saleheen-muhammad-mustak-hieFj0PZ-Jk-unsplash.jpg",
                created_at=datetime(2025, 1, 10, 16, 0, 0),
                updated_at=datetime(2025, 1, 10, 16, 0, 0),
            ),
            Artist(
                id=uuid.UUID(ARTIST8_ID),
                real_name="Vishnu R Nair",
                performing_name="Vishnu",
                date_of_birth=date(1992, 1, 1),
                photo_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/artists/vishnu-r-nair-kWCHq48Xwgw-unsplash.jpg",
                created_at=datetime(2025, 1, 10, 17, 0, 0),
                updated_at=datetime(2025, 1, 10, 17, 0, 0),
            ),
        ]
        db.add_all(artists)
        db.flush()
        print(f"    Created {len(artists)} artists")

        # 3. GENRES
        print("  Creating genres...")
        genres = [
            Genre(
                id=uuid.UUID(GENRE1_ID),
                name="Jazz",
                description="Jazz music",
                created_at=datetime(2025, 1, 5, 10, 0, 0),
                updated_at=datetime(2025, 1, 5, 10, 0, 0),
            ),
            Genre(
                id=uuid.UUID(GENRE2_ID),
                name="Rock",
                description="Rock music",
                created_at=datetime(2025, 1, 5, 10, 1, 0),
                updated_at=datetime(2025, 1, 5, 10, 1, 0),
            ),
            Genre(
                id=uuid.UUID(GENRE3_ID),
                name="Classical",
                description="Classical music",
                created_at=datetime(2025, 1, 5, 10, 2, 0),
                updated_at=datetime(2025, 1, 5, 10, 2, 0),
            ),
            Genre(
                id=uuid.UUID(GENRE4_ID),
                name="Hip Hop",
                description="Hip hop music",
                created_at=datetime(2025, 1, 5, 10, 3, 0),
                updated_at=datetime(2025, 1, 5, 10, 3, 0),
            ),
            Genre(
                id=uuid.UUID(GENRE5_ID),
                name="Blues",
                description="Blues music",
                created_at=datetime(2025, 1, 5, 10, 4, 0),
                updated_at=datetime(2025, 1, 5, 10, 4, 0),
            ),
            Genre(
                id=uuid.UUID(GENRE6_ID),
                name="Electronic",
                description="Electronic music",
                created_at=datetime(2025, 1, 5, 10, 5, 0),
                updated_at=datetime(2025, 1, 5, 10, 5, 0),
            ),
            Genre(
                id=uuid.UUID(GENRE7_ID),
                name="R&B",
                description="Rhythm and Blues",
                created_at=datetime(2025, 1, 5, 10, 6, 0),
                updated_at=datetime(2025, 1, 5, 10, 6, 0),
            ),
            Genre(
                id=uuid.UUID(GENRE8_ID),
                name="Pop",
                description="Pop music",
                created_at=datetime(2025, 1, 5, 10, 7, 0),
                updated_at=datetime(2025, 1, 5, 10, 7, 0),
            ),
        ]
        db.add_all(genres)
        db.flush()
        print(f"    Created {len(genres)} genres")

        # 4. ALBUMS
        print("  Creating albums...")
        albums = [
            Album(
                id=uuid.UUID(ALBUM1_ID),
                artist_id=uuid.UUID(ARTIST1_ID),
                name="A Love Supreme",
                price=19.99,
                release_date=date(1965, 1, 1),
                cover_image_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/albums/brett-jordan-x3wDxZJx9qs-unsplash.jpg",
                created_at=datetime(2025, 2, 1, 10, 0, 0),
                updated_at=datetime(2025, 2, 1, 10, 0, 0),
            ),
            Album(
                id=uuid.UUID(ALBUM2_ID),
                artist_id=uuid.UUID(ARTIST2_ID),
                name="Kind of Blue",
                price=18.99,
                release_date=date(1959, 8, 17),
                cover_image_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/albums/giorgio-trovato-PdtApuzR_IQ-unsplash.jpg",
                created_at=datetime(2025, 2, 1, 11, 0, 0),
                updated_at=datetime(2025, 2, 1, 11, 0, 0),
            ),
            Album(
                id=uuid.UUID(ALBUM3_ID),
                artist_id=uuid.UUID(ARTIST3_ID),
                name="The Dark Side of the Moon",
                price=21.99,
                release_date=date(1973, 3, 1),
                cover_image_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/albums/ivan-dorofeev-bsLXJsucvxc-unsplash.jpg",
                created_at=datetime(2025, 2, 1, 12, 0, 0),
                updated_at=datetime(2025, 2, 1, 12, 0, 0),
            ),
            Album(
                id=uuid.UUID(ALBUM4_ID),
                artist_id=uuid.UUID(ARTIST4_ID),
                name="OK Computer",
                price=20.99,
                release_date=date(1997, 5, 21),
                cover_image_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/albums/kobu-agency-3hWg9QKl5k8-unsplash.jpg",
                created_at=datetime(2025, 2, 1, 13, 0, 0),
                updated_at=datetime(2025, 2, 1, 13, 0, 0),
            ),
            Album(
                id=uuid.UUID(ALBUM5_ID),
                artist_id=uuid.UUID(ARTIST4_ID),
                name="Kid A",
                price=19.99,
                release_date=date(2000, 10, 2),
                cover_image_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/albums/seyi-ariyo-6YgYRcyQK_s-unsplash.jpg",
                created_at=datetime(2025, 2, 1, 14, 0, 0),
                updated_at=datetime(2025, 2, 1, 14, 0, 0),
            ),
            Album(
                id=uuid.UUID(ALBUM6_ID),
                artist_id=uuid.UUID(ARTIST5_ID),
                name="Live at the Apollo",
                price=17.99,
                release_date=date(1963, 5, 1),
                cover_image_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/albums/brett-jordan-x3wDxZJx9qs-unsplash.jpg",
                created_at=datetime(2025, 2, 1, 15, 0, 0),
                updated_at=datetime(2025, 2, 1, 15, 0, 0),
            ),
            Album(
                id=uuid.UUID(ALBUM7_ID),
                artist_id=uuid.UUID(ARTIST6_ID),
                name="Random Access Memories",
                price=22.99,
                release_date=date(2013, 5, 17),
                cover_image_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/albums/giorgio-trovato-PdtApuzR_IQ-unsplash.jpg",
                created_at=datetime(2025, 2, 1, 16, 0, 0),
                updated_at=datetime(2025, 2, 1, 16, 0, 0),
            ),
            Album(
                id=uuid.UUID(ALBUM8_ID),
                artist_id=uuid.UUID(ARTIST6_ID),
                name="Discovery",
                price=21.99,
                release_date=date(2001, 2, 26),
                cover_image_url="https://music-marketplace-images.s3.us-east-1.amazonaws.com/albums/ivan-dorofeev-bsLXJsucvxc-unsplash.jpg",
                created_at=datetime(2025, 2, 1, 17, 0, 0),
                updated_at=datetime(2025, 2, 1, 17, 0, 0),
            ),
        ]
        db.add_all(albums)
        db.flush()
        print(f"    Created {len(albums)} albums")

        # 5. ALBUM_GENRES
        print("  Creating album-genre associations...")
        album_genre_data = [
            (ALBUM1_ID, GENRE1_ID),  # A Love Supreme - Jazz
            (ALBUM2_ID, GENRE1_ID),  # Kind of Blue - Jazz
            (ALBUM3_ID, GENRE2_ID),  # The Dark Side of the Moon - Rock
            (ALBUM4_ID, GENRE2_ID),  # OK Computer - Rock
            (ALBUM5_ID, GENRE6_ID),  # Kid A - Electronic
            (ALBUM5_ID, GENRE7_ID),  # Kid A - Pop
            (ALBUM6_ID, GENRE5_ID),  # Live at the Apollo - Blues
            (ALBUM6_ID, GENRE8_ID),  # Live at the Apollo - R&B
            (ALBUM7_ID, GENRE6_ID),  # Random Access Memories - Electronic
            (ALBUM7_ID, GENRE7_ID),  # Random Access Memories - Pop
            (ALBUM8_ID, GENRE6_ID),  # Discovery - Electronic
            (ALBUM8_ID, GENRE7_ID),  # Discovery - Pop
        ]
        for album_id, genre_id in album_genre_data:
            db.add(AlbumGenre(
                album_id=uuid.UUID(album_id),
                genre_id=uuid.UUID(genre_id),
            ))
        db.flush()
        print(f"    Created {len(album_genre_data)} album-genre associations")

        # 6. TRACKS
        print("  Creating tracks...")
        tracks = [
            Track(
                id=uuid.UUID(TRACK1_ID),
                name="Acknowledgement",
                date=date(1965, 1, 1),
                album_id=uuid.UUID(ALBUM1_ID),
                created_at=datetime(2025, 2, 15, 10, 0, 0),
            ),
            Track(
                id=uuid.UUID(TRACK2_ID),
                name="Resolution",
                date=date(1965, 1, 1),
                album_id=uuid.UUID(ALBUM1_ID),
                created_at=datetime(2025, 2, 15, 10, 1, 0),
            ),
            Track(
                id=uuid.UUID(TRACK3_ID),
                name="Pursuance",
                date=date(1965, 1, 1),
                album_id=uuid.UUID(ALBUM1_ID),
                created_at=datetime(2025, 2, 15, 10, 2, 0),
            ),
            Track(
                id=uuid.UUID(TRACK4_ID),
                name="So What",
                date=date(1959, 8, 17),
                album_id=uuid.UUID(ALBUM2_ID),
                created_at=datetime(2025, 2, 15, 11, 0, 0),
            ),
            Track(
                id=uuid.UUID(TRACK5_ID),
                name="All Blues",
                date=date(1959, 8, 17),
                album_id=uuid.UUID(ALBUM2_ID),
                created_at=datetime(2025, 2, 15, 11, 1, 0),
            ),
            Track(
                id=uuid.UUID(TRACK6_ID),
                name="Speak to Me",
                date=date(1973, 3, 1),
                album_id=uuid.UUID(ALBUM3_ID),
                created_at=datetime(2025, 2, 15, 12, 0, 0),
            ),
            Track(
                id=uuid.UUID(TRACK7_ID),
                name="Breathe",
                date=date(1973, 3, 1),
                album_id=uuid.UUID(ALBUM3_ID),
                created_at=datetime(2025, 2, 15, 12, 1, 0),
            ),
            Track(
                id=uuid.UUID(TRACK8_ID),
                name="Time",
                date=date(1973, 3, 1),
                album_id=uuid.UUID(ALBUM3_ID),
                created_at=datetime(2025, 2, 15, 12, 2, 0),
            ),
            Track(
                id=uuid.UUID(TRACK9_ID),
                name="Airbag",
                date=date(1997, 5, 21),
                album_id=uuid.UUID(ALBUM4_ID),
                created_at=datetime(2025, 2, 15, 13, 0, 0),
            ),
            Track(
                id=uuid.UUID(TRACK10_ID),
                name="Paranoid Android",
                date=date(1997, 5, 21),
                album_id=uuid.UUID(ALBUM4_ID),
                created_at=datetime(2025, 2, 15, 13, 1, 0),
            ),
            Track(
                id=uuid.UUID(TRACK11_ID),
                name="Everything in Its Right Place",
                date=date(2000, 10, 2),
                album_id=uuid.UUID(ALBUM5_ID),
                created_at=datetime(2025, 2, 15, 14, 0, 0),
            ),
            Track(
                id=uuid.UUID(TRACK12_ID),
                name="Kid A",
                date=date(2000, 10, 2),
                album_id=uuid.UUID(ALBUM5_ID),
                created_at=datetime(2025, 2, 15, 14, 1, 0),
            ),
            Track(
                id=uuid.UUID(TRACK13_ID),
                name="Get Lucky",
                date=date(2013, 5, 17),
                album_id=uuid.UUID(ALBUM7_ID),
                created_at=datetime(2025, 2, 15, 16, 0, 0),
            ),
            Track(
                id=uuid.UUID(TRACK14_ID),
                name="Lose Yourself to Dance",
                date=date(2013, 5, 17),
                album_id=uuid.UUID(ALBUM7_ID),
                created_at=datetime(2025, 2, 15, 16, 1, 0),
            ),
            Track(
                id=uuid.UUID(TRACK15_ID),
                name="One More Time",
                date=date(2001, 2, 26),
                album_id=uuid.UUID(ALBUM8_ID),
                created_at=datetime(2025, 2, 15, 17, 0, 0),
            ),
            Track(
                id=uuid.UUID(TRACK16_ID),
                name="Digital Love",
                date=date(2001, 2, 26),
                album_id=uuid.UUID(ALBUM8_ID),
                created_at=datetime(2025, 2, 15, 17, 1, 0),
            ),
        ]
        db.add_all(tracks)
        db.flush()
        print(f"    Created {len(tracks)} tracks")

        # 7. PLAYLISTS
        print("  Creating playlists...")
        playlists = [
            Playlist(
                id=uuid.UUID(PLAYLIST1_ID),
                user_id=uuid.UUID(USER1_ID),
                name="My Jazz Collection",
                created_at=datetime(2025, 3, 1, 10, 0, 0),
            ),
            Playlist(
                id=uuid.UUID(PLAYLIST2_ID),
                user_id=uuid.UUID(USER1_ID),
                name="Electronic Vibes",
                created_at=datetime(2025, 3, 1, 11, 0, 0),
            ),
            Playlist(
                id=uuid.UUID(PLAYLIST3_ID),
                user_id=uuid.UUID(USER2_ID),
                name="Rock Classics",
                created_at=datetime(2025, 3, 2, 10, 0, 0),
            ),
        ]
        db.add_all(playlists)
        db.flush()
        print(f"    Created {len(playlists)} playlists")

        # 8. PLAYLIST_TRACKS
        print("  Adding tracks to playlists...")
        playlist_tracks_data = [
            PlaylistTrack(
                id=uuid.UUID(PTRACK1_ID),
                playlist_id=uuid.UUID(PLAYLIST1_ID),
                track_id=uuid.UUID(TRACK1_ID),
                created_at=datetime(2025, 3, 5, 10, 0, 0),
            ),
            PlaylistTrack(
                id=uuid.UUID(PTRACK2_ID),
                playlist_id=uuid.UUID(PLAYLIST1_ID),
                track_id=uuid.UUID(TRACK2_ID),
                created_at=datetime(2025, 3, 5, 10, 1, 0),
            ),
            PlaylistTrack(
                id=uuid.UUID(PTRACK3_ID),
                playlist_id=uuid.UUID(PLAYLIST1_ID),
                track_id=uuid.UUID(TRACK4_ID),
                created_at=datetime(2025, 3, 5, 10, 2, 0),
            ),
            PlaylistTrack(
                id=uuid.UUID(PTRACK4_ID),
                playlist_id=uuid.UUID(PLAYLIST2_ID),
                track_id=uuid.UUID(TRACK13_ID),
                created_at=datetime(2025, 3, 6, 10, 0, 0),
            ),
            PlaylistTrack(
                id=uuid.UUID(PTRACK5_ID),
                playlist_id=uuid.UUID(PLAYLIST2_ID),
                track_id=uuid.UUID(TRACK15_ID),
                created_at=datetime(2025, 3, 6, 10, 1, 0),
            ),
            PlaylistTrack(
                id=uuid.UUID(PTRACK6_ID),
                playlist_id=uuid.UUID(PLAYLIST2_ID),
                track_id=uuid.UUID(TRACK11_ID),
                created_at=datetime(2025, 3, 6, 10, 2, 0),
            ),
            PlaylistTrack(
                id=uuid.UUID(PTRACK7_ID),
                playlist_id=uuid.UUID(PLAYLIST3_ID),
                track_id=uuid.UUID(TRACK8_ID),
                created_at=datetime(2025, 3, 7, 10, 0, 0),
            ),
            PlaylistTrack(
                id=uuid.UUID(PTRACK8_ID),
                playlist_id=uuid.UUID(PLAYLIST3_ID),
                track_id=uuid.UUID(TRACK9_ID),
                created_at=datetime(2025, 3, 7, 10, 1, 0),
            ),
        ]
        db.add_all(playlist_tracks_data)
        db.flush()
        print(f"    Added {len(playlist_tracks_data)} tracks to playlists")

        # 9. PURCHASES
        print("  Creating purchases...")
        purchases = [
            Purchase(
                id=uuid.UUID(PURCHASE1_ID),
                user_id=uuid.UUID(USER1_ID),
                album_id=uuid.UUID(ALBUM1_ID),
                purchase_date=datetime(2025, 4, 1, 10, 0, 0),
                amount_paid=19.99,
            ),
            Purchase(
                id=uuid.UUID(PURCHASE2_ID),
                user_id=uuid.UUID(USER1_ID),
                album_id=uuid.UUID(ALBUM2_ID),
                purchase_date=datetime(2025, 4, 2, 10, 0, 0),
                amount_paid=18.99,
            ),
            Purchase(
                id=uuid.UUID(PURCHASE3_ID),
                user_id=uuid.UUID(USER1_ID),
                album_id=uuid.UUID(ALBUM7_ID),
                purchase_date=datetime(2025, 4, 3, 10, 0, 0),
                amount_paid=22.99,
            ),
            Purchase(
                id=uuid.UUID(PURCHASE4_ID),
                user_id=uuid.UUID(USER2_ID),
                album_id=uuid.UUID(ALBUM3_ID),
                purchase_date=datetime(2025, 4, 5, 10, 0, 0),
                amount_paid=21.99,
            ),
            Purchase(
                id=uuid.UUID(PURCHASE5_ID),
                user_id=uuid.UUID(USER2_ID),
                album_id=uuid.UUID(ALBUM4_ID),
                purchase_date=datetime(2025, 4, 6, 10, 0, 0),
                amount_paid=20.99,
            ),
            Purchase(
                id=uuid.UUID(PURCHASE6_ID),
                user_id=uuid.UUID(USER2_ID),
                album_id=uuid.UUID(ALBUM5_ID),
                purchase_date=datetime(2025, 4, 7, 10, 0, 0),
                amount_paid=19.99,
            ),
        ]
        db.add_all(purchases)
        db.flush()
        print(f"    Created {len(purchases)} purchases")

        # 10. RATINGS
        print("  Creating ratings...")
        ratings = [
            Rating(
                id=uuid.UUID(RATING1_ID),
                user_id=uuid.UUID(USER1_ID),
                album_id=uuid.UUID(ALBUM1_ID),
                rating=5,
                created_at=datetime(2025, 4, 10, 10, 0, 0),
                updated_at=datetime(2025, 4, 10, 10, 0, 0),
            ),
            Rating(
                id=uuid.UUID(RATING2_ID),
                user_id=uuid.UUID(USER1_ID),
                album_id=uuid.UUID(ALBUM2_ID),
                rating=5,
                created_at=datetime(2025, 4, 11, 10, 0, 0),
                updated_at=datetime(2025, 4, 11, 10, 0, 0),
            ),
            Rating(
                id=uuid.UUID(RATING3_ID),
                user_id=uuid.UUID(USER1_ID),
                album_id=uuid.UUID(ALBUM7_ID),
                rating=4,
                created_at=datetime(2025, 4, 12, 10, 0, 0),
                updated_at=datetime(2025, 4, 12, 10, 0, 0),
            ),
            Rating(
                id=uuid.UUID(RATING4_ID),
                user_id=uuid.UUID(USER2_ID),
                album_id=uuid.UUID(ALBUM3_ID),
                rating=5,
                created_at=datetime(2025, 4, 15, 10, 0, 0),
                updated_at=datetime(2025, 4, 15, 10, 0, 0),
            ),
            Rating(
                id=uuid.UUID(RATING5_ID),
                user_id=uuid.UUID(USER2_ID),
                album_id=uuid.UUID(ALBUM4_ID),
                rating=5,
                created_at=datetime(2025, 4, 16, 10, 0, 0),
                updated_at=datetime(2025, 4, 16, 10, 0, 0),
            ),
            Rating(
                id=uuid.UUID(RATING6_ID),
                user_id=uuid.UUID(USER2_ID),
                album_id=uuid.UUID(ALBUM5_ID),
                rating=4,
                created_at=datetime(2025, 4, 17, 10, 0, 0),
                updated_at=datetime(2025, 4, 17, 10, 0, 0),
            ),
        ]
        db.add_all(ratings)
        db.flush()
        print(f"    Created {len(ratings)} ratings")

        # Commit all changes
        db.commit()
        print("\nSeed completed successfully!")
        print(f"  Users: {db.query(User).count()}")
        print(f"  Artists: {db.query(Artist).count()}")
        print(f"  Genres: {db.query(Genre).count()}")
        print(f"  Albums: {db.query(Album).count()}")
        print(f"  Tracks: {db.query(Track).count()}")
        print(f"  Playlists: {db.query(Playlist).count()}")
        print(f"  Purchases: {db.query(Purchase).count()}")
        print(f"  Ratings: {db.query(Rating).count()}")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
