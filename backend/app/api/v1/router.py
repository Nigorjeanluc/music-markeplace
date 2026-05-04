from fastapi import APIRouter
from app.api.v1.endpoints import auth, artists, albums, purchases, ratings, genres, tracks, playlists, upload

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(artists.router, prefix="/artists", tags=["artists"])
api_router.include_router(albums.router, prefix="/albums", tags=["albums"])
api_router.include_router(purchases.router, prefix="/purchases", tags=["purchases"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
api_router.include_router(genres.router, prefix="/genres", tags=["genres"])
api_router.include_router(tracks.router, prefix="/tracks", tags=["tracks"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
