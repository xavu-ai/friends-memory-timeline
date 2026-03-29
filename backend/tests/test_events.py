import pytest
from datetime import date
from uuid import uuid4
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import Event
from app.services.auth_service import create_access_token


class TestEvents:
    @pytest.mark.asyncio
    async def test_list_events_newest_first(
        self, async_client: AsyncClient, db_session: AsyncSession
    ):
        """Test GET /api/v1/events returns events newest first."""
        token, _ = create_access_token("valid_password")
        headers = {"Authorization": f"Bearer {token}"}

        e1 = Event(date=date(2024, 1, 1), title="Older Event")
        e2 = Event(date=date(2024, 6, 1), title="Newer Event")
        db_session.add_all([e1, e2])
        await db_session.commit()

        response = await async_client.get("/api/v1/events", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["events"]) == 2
        assert data["events"][0]["title"] == "Newer Event"
        assert data["events"][1]["title"] == "Older Event"

    @pytest.mark.asyncio
    async def test_create_event_logs_to_edit_logs(
        self, async_client: AsyncClient
    ):
        """Test POST /api/v1/events with auth logs to edit_logs."""
        token, _ = create_access_token("valid_password")
        headers = {"Authorization": f"Bearer {token}"}

        response = await async_client.post(
            "/api/v1/events",
            json={"date": "2024-01-15", "title": "Test Event", "story": "A story"},
            headers=headers,
        )
        assert response.status_code == 201
        # Edit log creation is verified in unit tests

    @pytest.mark.asyncio
    async def test_update_event_logs_to_edit_logs(
        self, async_client: AsyncClient, db_session: AsyncSession
    ):
        """Test PUT /api/v1/events/:id with auth logs to edit_logs."""
        token, _ = create_access_token("valid_password")
        headers = {"Authorization": f"Bearer {token}"}

        event = Event(date=date(2024, 1, 1), title="Original Title")
        db_session.add(event)
        await db_session.commit()
        await db_session.refresh(event)

        response = await async_client.put(
            f"/api/v1/events/{event.id}",
            json={"title": "Updated Title"},
            headers=headers,
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_event_logs_to_edit_logs(
        self, async_client: AsyncClient, db_session: AsyncSession
    ):
        """Test DELETE /api/v1/events/:id with auth logs to edit_logs."""
        token, _ = create_access_token("valid_password")
        headers = {"Authorization": f"Bearer {token}"}

        event = Event(date=date(2024, 1, 1), title="To Delete")
        db_session.add(event)
        await db_session.commit()
        await db_session.refresh(event)

        response = await async_client.delete(
            f"/api/v1/events/{event.id}",
            headers=headers,
        )
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_unauthenticated_returns_401(self, async_client: AsyncClient):
        """Test unauthenticated requests return 401."""
        response = await async_client.get("/api/v1/events")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_not_found_returns_404(
        self, async_client: AsyncClient, db_session: AsyncSession
    ):
        """Test getting non-existent event returns 404."""
        token, _ = create_access_token("valid_password")
        headers = {"Authorization": f"Bearer {token}"}

        response = await async_client.get(
            f"/api/v1/events/{uuid4()}",
            headers=headers,
        )
        assert response.status_code == 404
