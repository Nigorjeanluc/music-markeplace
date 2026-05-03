import pytest


class TestListAlbums:
    def test_public_access(self, client):
        response = client.get("/api/v1/albums/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_with_search(self, client):
        response = client.get("/api/v1/albums/?search=test")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data


class TestGetAlbum:
    def test_public_access(self, client):
        # Use valid UUID that doesn't exist
        response = client.get("/api/v1/albums/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestCreateAlbum:
    def test_admin_only(self, client, admin_token):
        # Create artist first
        artist_resp = client.post("/api/v1/artists/", json={
            "real_name": "Test Artist",
            "performing_name": "TestPerforming",
            "date_of_birth": "2000-01-01"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        artist_id = artist_resp.json()["id"]

        # Create album
        response = client.post("/api/v1/albums/", json={
            "name": "New Album",
            "price": 10.99,
            "artist_id": artist_id,
            "genre_ids": []
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["name"] == "New Album"

    def test_unauthorized(self, client):
        response = client.post("/api/v1/albums/", json={
            "name": "New Album",
            "price": 10.99,
            "artist_id": "some-id",
            "genre_ids": []
        })
        assert response.status_code == 401


class TestUpdateAlbum:
    def test_admin_only(self, client, admin_token):
        response = client.put("/api/v1/albums/nonexistent-id", json={
            "name": "Updated"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404

    def test_unauthorized(self, client):
        response = client.put("/api/v1/albums/some-id", json={"name": "Updated"})
        assert response.status_code == 401


class TestDeleteAlbum:
    def test_admin_only(self, client, admin_token):
        response = client.delete("/api/v1/albums/nonexistent-id", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 404

    def test_unauthorized(self, client):
        response = client.delete("/api/v1/albums/some-id")
        assert response.status_code == 401
