from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.core.security import get_current_admin_user
from app.services.genre_service import GenreService
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse

router = APIRouter()


@router.get("/", response_model=List[GenreResponse])
def list_genres(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all genres (public endpoint)."""
    genre_service = GenreService(db)
    genres = genre_service.get_genres(skip=skip, limit=limit, search=search)
    return [
        GenreResponse(
            id=str(g.id),
            name=g.name,
            description=g.description,
            created_at=g.created_at,
            updated_at=g.updated_at,
        )
        for g in genres
    ]


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(genre_id: str, db: Session = Depends(get_db)):
    """Get genre detail (public endpoint)."""
    genre_service = GenreService(db)
    genre = genre_service.get_genre(genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return GenreResponse(
        id=str(genre.id),
        name=genre.name,
        description=genre.description,
        created_at=genre.created_at,
        updated_at=genre.updated_at,
    )


@router.post("/", response_model=GenreResponse)
def create_genre(
    genre_in: GenreCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Create a new genre (admin only)."""
    genre_service = GenreService(db)
    if genre_service.get_genres(search=genre_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre with this name already exists"
        )
    genre = genre_service.create_genre(genre_in)
    return GenreResponse(
        id=str(genre.id),
        name=genre.name,
        description=genre.description,
        created_at=genre.created_at,
        updated_at=genre.updated_at,
    )


@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(
    genre_id: str,
    genre_in: GenreUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Update a genre (admin only)."""
    genre_service = GenreService(db)
    genre = genre_service.update_genre(genre_id, genre_in)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return GenreResponse(
        id=str(genre.id),
        name=genre.name,
        description=genre.description,
        created_at=genre.created_at,
        updated_at=genre.updated_at,
    )


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(
    genre_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    """Delete a genre (admin only)."""
    genre_service = GenreService(db)
    if not genre_service.delete_genre(genre_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
