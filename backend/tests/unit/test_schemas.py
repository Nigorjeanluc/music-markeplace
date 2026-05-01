import pytest
from pydantic import ValidationError
from app.schemas.user import UserLogin, UserCreate, UserResponse
from app.schemas.token import Token, TokenRefresh
from datetime import datetime


class TestUserLogin:
    def test_valid_email(self):
        user = UserLogin(email="test@example.com", password="password123")
        assert user.email == "test@example.com"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserLogin(email="not-an-email", password="password123")

    def test_missing_password(self):
        with pytest.raises(ValidationError):
            UserLogin(email="test@example.com")


class TestUserCreate:
    def test_valid_data(self):
        user = UserCreate(email="test@example.com", username="testuser", password="password123")
        assert user.email == "test@example.com"
        assert user.username == "testuser"

    def test_missing_fields(self):
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com")

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreate(email="invalid", username="test", password="pass")


class TestToken:
    def test_token_valid(self):
        token = Token(access_token="abc", refresh_token="def", token_type="bearer")
        assert token.access_token == "abc"

    def test_token_default_type(self):
        token = Token(access_token="abc", refresh_token="def")
        assert token.token_type == "bearer"


class TestTokenRefresh:
    def test_valid_refresh_token(self):
        token = TokenRefresh(refresh_token="valid_refresh_token")
        assert token.refresh_token == "valid_refresh_token"

    def test_missing_refresh_token(self):
        with pytest.raises(ValidationError):
            TokenRefresh()
