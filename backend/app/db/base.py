from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 🔥 Import all models here so Alembic can detect them
from app.models.user import User
from app.models.artist import Artist
from app.models.album import Album
from app.models.purchase import Purchase
from app.models.rating import Rating
from app.models.track import Track
from app.models.playlist import Playlist
from app.models.playlist_track import PlaylistTrack