import pytest


class TestRegisterEndpoint:
    def test_successful_registration(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_duplicate_email(self, client, normal_user):
        response = client.post("/api/v1/auth/register", json={
            "email": normal_user.email,  # Already exists
            "username": "anotheruser",
            "password": "password123"
        })
        assert response.status_code == 400

    def test_duplicate_username(self, client, normal_user):
        response = client.post("/api/v1/auth/register", json={
            "email": "another@example.com",
            "username": normal_user.username,  # Already exists
            "password": "password123"
        })
        assert response.status_code == 400


class TestLoginEndpoint:
    def test_successful_login(self, client):
        # First register
        client.post("/api/v1/auth/register", json={
            "email": "logintest@example.com",
            "username": "logintest",
            "password": "password123"
        })
        # Then login
        response = client.post("/api/v1/auth/login", json={
            "email": "logintest@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_incorrect_password(self, client):
        # Register first
        client.post("/api/v1/auth/register", json={
            "email": "logintest2@example.com",
            "username": "logintest2",
            "password": "password123"
        })
        # Wrong password
        response = client.post("/api/v1/auth/login", json={
            "email": "logintest2@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_nonexistent_email(self, client):
        response = client.post("/api/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "password123"
        })
        assert response.status_code == 401


class TestRefreshTokenEndpoint:
    def test_successful_refresh(self, client):
        # Register to get tokens
        response = client.post("/api/v1/auth/register", json={
            "email": "refreshtest@example.com",
            "username": "refreshtest",
            "password": "password123"
        })
        tokens = response.json()
        refresh_token = tokens["refresh_token"]

        # Refresh
        response = client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert response.status_code == 200
        new_tokens = response.json()
        assert "access_token" in new_tokens

    def test_invalid_refresh_token(self, client):
        response = client.post("/api/v1/auth/refresh", json={
            "refresh_token": "invalid_token"
        })
        assert response.status_code == 401


class TestMeEndpoint:
    def test_authenticated(self, client, user_token, normal_user):
        response = client.get("/api/v1/auth/me", headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == normal_user.email

    def test_unauthenticated(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
