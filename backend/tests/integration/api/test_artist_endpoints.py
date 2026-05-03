import pytest


class TestListArtists:
    def test_public_access(self, client):
        response = client.get("/api/v1/artists/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_with_search(self, client):
        response = client.get("/api/v1/artists/?search=test")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data


class TestGetArtist:
    def test_public_access(self, client):
        response = client.get("/api/v1/artists/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestCreateArtist:
    def test_admin_only(self, client, admin_token):
        response = client.post("/api/v1/artists/", json={
            "real_name": "New Artist",
            "performing_name": "New Performing",
            "date_of_birth": "2000-01-01"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["performing_name"] == "New Performing"

    def test_unauthorized(self, client):
        response = client.post("/api/v1/artists/", json={
            "real_name": "New Artist",
            "performing_name": "New Performing"
        })
        assert response.status_code == 401

    def test_duplicate_performing_name(self, client, admin_token):
        # Create first
        client.post("/api/v1/artists/", json={
            "real_name": "Duplicate",
            "performing_name": "UniquePerformingName"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        # Try again
        response = client.post("/api/v1/artists/", json={
            "real_name": "Duplicate2",
            "performing_name": "UniquePerformingName"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        # May fail if unique constraint exists


class TestUpdateArtist:
    def test_admin_only(self, client, admin_token):
        # Create artist first
        create_resp = client.post("/api/v1/artists/", json={
            "real_name": "To Update",
            "performing_name": "UpdatePerforming",
            "date_of_birth": "2000-01-01"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        artist_id = create_resp.json()["id"]

        # Update
        response = client.put(f"/api/v1/artists/{artist_id}", json={
            "performing_name": "UpdatedPerforming"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["performing_name"] == "UpdatedPerforming"

    def test_unauthorized(self, client):
        response = client.put("/api/v1/artists/some-id", json={"performing_name": "Updated"})
        assert response.status_code == 401


class TestDeleteArtist:
    def test_admin_only(self, client, admin_token):
        # Create artist first
        create_resp = client.post("/api/v1/artists/", json={
            "real_name": "To Delete",
            "performing_name": "DeletePerforming",
            "date_of_birth": "2000-01-01"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        artist_id = create_resp.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/artists/{artist_id}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 204

    def test_unauthorized(self, client):
        response = client.delete("/api/v1/artists/some-id")
        assert response.status_code == 401
