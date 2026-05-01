import pytest


class TestListGenres:
    def test_public_access(self, client):
        response = client.get("/api/v1/genres/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_with_search(self, client):
        response = client.get("/api/v1/genres/?search=rock")
        assert response.status_code == 200


class TestGetGenre:
    def test_public_access(self, client):
        response = client.get("/api/v1/genres/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestCreateGenre:
    def test_admin_only(self, client, admin_token):
        response = client.post("/api/v1/genres/", json={
            "name": "New Genre",
            "description": "Test"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Genre"

    def test_unauthorized(self, client):
        response = client.post("/api/v1/genres/", json={
            "name": "New Genre"
        })
        assert response.status_code == 401


class TestUpdateGenre:
    def test_admin_only(self, client, admin_token):
        # Create first
        create = client.post("/api/v1/genres/", json={
            "name": "To Update"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        genre_id = create.json()["id"]

        # Update
        response = client.put(f"/api/v1/genres/{genre_id}", json={
            "name": "Updated Genre"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Genre"

    def test_unauthorized(self, client):
        response = client.put("/api/v1/genres/some-id", json={"name": "Updated"})
        assert response.status_code == 401


class TestDeleteGenre:
    def test_admin_only(self, client, admin_token):
        # Create first
        create = client.post("/api/v1/genres/", json={
            "name": "To Delete"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        genre_id = create.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/genres/{genre_id}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 204

    def test_unauthorized(self, client):
        response = client.delete("/api/v1/genres/some-id")
        assert response.status_code == 401
