import pytest
from uuid import uuid4


class TestEventsIntegration:
    @pytest.mark.asyncio
    async def test_create_event_requires_auth(self, async_client):
        """Test that creating an event without auth returns 401."""
        response = await async_client.post(
            "/api/v1/events",
            json={"title": "Test", "date": "2024-01-15"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_list_events_requires_auth(self, async_client):
        """Test that listing events without auth returns 401."""
        response = await async_client.get("/api/v1/events")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_event_requires_auth(self, async_client):
        """Test that getting an event without auth returns 401."""
        response = await async_client.get(
            f"/api/v1/events/{uuid4()}"
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_delete_event_requires_auth(self, async_client):
        """Test that deleting an event without auth returns 401."""
        response = await async_client.delete(
            f"/api/v1/events/{uuid4()}"
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_event_with_auth(
        self, async_client, auth_headers
    ):
        """Test creating an event with valid auth."""
        response = await async_client.post(
            "/api/v1/events",
            json={
                "title": "Test Event",
                "date": "2024-01-15",
                "story": "A wonderful day",
                "location": "Paris",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Event"
        assert data["date"] == "2024-01-15"

    @pytest.mark.asyncio
    async def test_list_events_with_pagination(
        self, async_client, auth_headers
    ):
        """Test listing events with pagination."""
        for i in range(3):
            await async_client.post(
                "/api/v1/events",
                json={"title": f"Event {i}", "date": f"2024-01-{i+1:02d}"},
                headers=auth_headers,
            )

        response = await async_client.get(
            "/api/v1/events?limit=2&offset=0",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["events"]) == 2

    @pytest.mark.asyncio
    async def test_get_event_not_found(
        self, async_client, auth_headers
    ):
        """Test getting non-existent event returns 404."""
        response = await async_client.get(
            f"/api/v1/events/{uuid4()}",
            headers=auth_headers,
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_event(
        self, async_client, auth_headers
    ):
        """Test updating an event."""
        create_resp = await async_client.post(
            "/api/v1/events",
            json={"title": "Original", "date": "2024-01-01"},
            headers=auth_headers,
        )
        event_id = create_resp.json()["id"]

        update_resp = await async_client.put(
            f"/api/v1/events/{event_id}",
            json={"title": "Updated"},
            headers=auth_headers,
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["title"] == "Updated"

    @pytest.mark.asyncio
    async def test_delete_event(
        self, async_client, auth_headers
    ):
        """Test deleting an event."""
        create_resp = await async_client.post(
            "/api/v1/events",
            json={"title": "To Delete", "date": "2024-01-01"},
            headers=auth_headers,
        )
        event_id = create_resp.json()["id"]

        delete_resp = await async_client.delete(
            f"/api/v1/events/{event_id}",
            headers=auth_headers,
        )
        assert delete_resp.status_code == 204

        get_resp = await async_client.get(
            f"/api/v1/events/{event_id}",
            headers=auth_headers,
        )
        assert get_resp.status_code == 404
