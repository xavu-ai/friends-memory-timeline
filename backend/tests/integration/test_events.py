import pytest
from unittest.mock import patch


class TestEvents:
    @pytest.mark.asyncio
    async def test_create_event_requires_auth(self, async_client):
        """Test that creating an event without auth returns 401."""
        response = await async_client.post(
            "/api/v1/events",
            data={"title": "Test", "date": "2024-01-15"},
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
        response = await async_client.get("/api/v1/events/00000000-0000-0000-0000-000000000001")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_delete_event_requires_auth(self, async_client):
        """Test that deleting an event without auth returns 401."""
        response = await async_client.delete("/api/v1/events/00000000-0000-0000-0000-000000000001")
        assert response.status_code == 401
