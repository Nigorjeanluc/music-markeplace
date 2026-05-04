import pytest
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token


class TestAuthServiceRegister:
    def test_successful_registration(self, db_session):
        auth_service = AuthService(db_session)
        user_in = UserCreate(email="newuser@example.com", username="newuser", password="password123")
        user, tokens = auth_service.register(user_in)

        assert user.email == "newuser@example.com"
        assert user.username == "newuser"
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"

    def test_duplicate_email(self, db_session, normal_user):
        auth_service = AuthService(db_session)
        user_in = UserCreate(email=normal_user.email, username="anotheruser", password="password123")
        with pytest.raises(HTTPException) as exc_info:
            auth_service.register(user_in)
        assert exc_info.value.status_code == 400

    def test_duplicate_username(self, db_session, normal_user):
        auth_service = AuthService(db_session)
        user_in = UserCreate(email="another@example.com", username=normal_user.username, password="password123")
        with pytest.raises(HTTPException) as exc_info:
            auth_service.register(user_in)
        assert exc_info.value.status_code == 400


class TestAuthServiceLogin:
    def test_successful_login(self, db_session, normal_user):
        auth_service = AuthService(db_session)
        user_in = UserLogin(email=normal_user.email, password="testpassword123")
        result = auth_service.login(user_in)

        assert result is not None
        user, tokens = result
        assert user.email == normal_user.email
        assert "access_token" in tokens

    def test_incorrect_password(self, db_session, normal_user):
        auth_service = AuthService(db_session)
        user_in = UserLogin(email="testuser@example.com", password="wrongpassword")
        result = auth_service.login(user_in)
        assert result is None

    def test_incorrect_email(self, db_session):
        auth_service = AuthService(db_session)
        user_in = UserLogin(email="nonexistent@example.com", password="password123")
        result = auth_service.login(user_in)
        assert result is None


class TestAuthServiceRefreshToken:
    def test_valid_refresh_token(self, db_session, normal_user, user_token):
        from app.core.security import create_refresh_token
        from app.schemas.token import TokenRefresh
        auth_service = AuthService(db_session)
        # Create a refresh token for the user
        refresh_token_str = create_refresh_token({"sub": str(normal_user.id)})
        token_in = TokenRefresh(refresh_token=refresh_token_str)
        result = auth_service.refresh_token(token_in)

        assert result is not None
        user, tokens = result
        assert user.id == normal_user.id
        assert "access_token" in tokens
        assert "refresh_token" in tokens

    def test_invalid_refresh_token(self, db_session):
        from app.schemas.token import TokenRefresh
        auth_service = AuthService(db_session)
        token_in = TokenRefresh(refresh_token="invalid_token")
        result = auth_service.refresh_token(token_in)
        assert result is None


class TestAuthServiceGetCurrentUserResponse:
    def test_convert_user_to_response(self, normal_user):
        auth_service = AuthService(None)
        response = auth_service.get_current_user_response(normal_user)

        assert response.id == str(normal_user.id)
        assert response.email == normal_user.email
        assert response.username == normal_user.username
        assert response.is_active == normal_user.is_active
        assert response.is_admin == normal_user.is_admin
