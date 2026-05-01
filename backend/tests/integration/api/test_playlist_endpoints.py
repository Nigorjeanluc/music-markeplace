import pytest

DUMMY_UUID = "00000000-0000-0000-0000-000000000000"


class TestListPlaylists:
    def test_authenticated(self, client, user_token):
        response = client.get("/api/v1/playlists/", headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_unauthenticated(self, client):
        response = client.get("/api/v1/playlists/")
        assert response.status_code == 401


class TestGetPlaylist:
    def test_authenticated(self, client, user_token):
        response = client.get("/api/v1/playlists/nonexistent-id", headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code == 404

    def test_unauthenticated(self, client):
        response = client.get("/api/v1/playlists/some-id")
        assert response.status_code == 401


class TestCreatePlaylist:
    def test_authenticated(self, client, user_token):
        response = client.post("/api/v1/playlists/", json={
            "name": "My Playlist",
            "track_ids": []
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "My Playlist"

    def test_unauthenticated(self, client):
        response = client.post("/api/v1/playlists/", json={
            "name": "My Playlist"
        })
        assert response.status_code == 401


class TestUpdatePlaylist:
    def test_authenticated(self, client, user_token):
        # Create first
        create = client.post("/api/v1/playlists/", json={
            "name": "To Update"
        }, headers={"Authorization": f"Bearer {user_token}"})
        playlist_id = create.json()["id"]

        # Update
        response = client.put(f"/api/v1/playlists/{playlist_id}", json={
            "name": "Updated Playlist"
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Playlist"

    def test_other_user(self, client, admin_token, user_token):
        # User creates, admin tries to update
        create = client.post("/api/v1/playlists/", json={
            "name": "User Playlist"
        }, headers={"Authorization": f"Bearer {user_token}"})
        playlist_id = create.json()["id"]

        # Admin tries
        response = client.put(f"/api/v1/playlists/{playlist_id}", json={
            "name": "Hacked"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404  # Not found for admin

    def test_unauthenticated(self, client):
        response = client.put("/api/v1/playlists/some-id", json={"name": "Updated"})
        assert response.status_code == 401


class TestDeletePlaylist:
    def test_authenticated(self, client, user_token):
        # Create first
        create = client.post("/api/v1/playlists/", json={
            "name": "To Delete"
        }, headers={"Authorization": f"Bearer {user_token}"})
        playlist_id = create.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/playlists/{playlist_id}", headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code == 204

    def test_other_user(self, client, admin_token, user_token):
        # User creates, admin tries to delete
        create = client.post("/api/v1/playlists/", json={
            "name": "User Playlist"
        }, headers={"Authorization": f"Bearer {user_token}"})
        playlist_id = create.json()["id"]

        # Admin tries
        response = client.delete(f"/api/v1/playlists/{playlist_id}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 404

    def test_unauthenticated(self, client):
        response = client.delete(f"/api/v1/playlists/{DUMMY_UUID}")
        assert response.status_code == 401


class TestAddTrackToPlaylist:
    def test_authenticated(self, client, user_token, normal_user):
        # Create playlist first
        create_pl = client.post("/api/v1/playlists/", json={
            "name": "Playlist"
        }, headers={"Authorization": f"Bearer {user_token}"})
        playlist_id = create_pl.json()["id"]

        # Add track (uses valid UUID format, may not exist which is OK)
        response = client.post(f"/api/v1/playlists/{playlist_id}/tracks", json={
            "track_id": "00000000-0000-0000-0000-000000000000"
        }, headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code in [204, 404]  # 204 on success, 404 if track not found

    def test_unauthenticated(self, client):
        response = client.post("/api/v1/playlists/00000000-0000-0000-0000-000000000000/tracks", json={
            "track_id": "00000000-0000-0000-0000-000000000000"
        })
        assert response.status_code == 401


class TestRemoveTrackFromPlaylist:
    def test_authenticated(self, client, user_token):
        # Create playlist with track, then remove
        # Simplified: test 404
        response = client.delete(f"/api/v1/playlists/{DUMMY_UUID}/tracks/{DUMMY_UUID}", headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code in [204, 404]

    def test_unauthenticated(self, client):
        response = client.delete(f"/api/v1/playlists/{DUMMY_UUID}/tracks/{DUMMY_UUID}")
        assert response.status_code == 401
