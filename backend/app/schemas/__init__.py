from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token, TokenRefresh
from app.schemas.artist import ArtistCreate, ArtistUpdate, ArtistResponse
from app.schemas.album import AlbumCreate, AlbumUpdate, AlbumResponse
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.schemas.rating import RatingCreate, RatingUpdate, RatingResponse
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse
from app.schemas.track import TrackCreate, TrackUpdate, TrackResponse
from app.schemas.playlist import (
    PlaylistCreate, PlaylistUpdate, PlaylistResponse, PlaylistDetailResponse,
    PlaylistTrackAdd
)

__all__ = [
    "UserCreate", "UserLogin", "UserResponse",
    "Token", "TokenRefresh",
    "ArtistCreate", "ArtistUpdate", "ArtistResponse",
    "AlbumCreate", "AlbumUpdate", "AlbumResponse",
    "PurchaseCreate", "PurchaseResponse",
    "RatingCreate", "RatingUpdate", "RatingResponse",
    "GenreCreate", "GenreUpdate", "GenreResponse",
    "TrackCreate", "TrackUpdate", "TrackResponse",
    "PlaylistCreate", "PlaylistUpdate", "PlaylistResponse",
    "PlaylistDetailResponse", "PlaylistTrackAdd",
]
