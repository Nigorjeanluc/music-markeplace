from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional, Tuple

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token, TokenRefresh
from app.core.security import (
    get_password_hash, verify_password,
    create_access_token, create_refresh_token, decode_token
)
from fastapi import HTTPException, status


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, user_in: UserCreate) -> Tuple[User, Token]:
        """Register a new user and return user with tokens."""
        # Check if user already exists
        if self.db.query(User).filter(User.email == user_in.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        if self.db.query(User).filter(User.username == user_in.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Create user
        user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            is_admin=False,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # Create tokens
        token_data = {"sub": str(user.id)}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
        return user, tokens

    def login(self, user_in: UserLogin) -> Optional[Tuple[User, Token]]:
        """Login user and return user with tokens if successful."""
        user = self.db.query(User).filter(User.email == user_in.email).first()
        if not user or not verify_password(user_in.password, user.hashed_password):
            return None

        token_data = {"sub": str(user.id)}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
        return user, tokens

    def refresh_token(self, token_in: TokenRefresh) -> Optional[Tuple[User, Token]]:
        """Refresh access token using refresh token."""
        payload = decode_token(token_in.refresh_token)
        if payload is None or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None

        token_data = {"sub": str(user.id)}
        access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)

        tokens = {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
        return user, tokens

    def get_current_user_response(self, user: User) -> UserResponse:
        """Convert User model to UserResponse schema."""
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
        )
