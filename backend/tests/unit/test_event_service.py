import pytest
from datetime import date
from uuid import uuid4
from app.services.event_service import create_event, get_event, list_events
from app.schemas.event import EventCreate


class TestEventService:
    @pytest.mark.asyncio
    async def test_create_event(self, db_session):
        """Test creating an event."""
        event_data = EventCreate(
            title="Test Event",
            event_date=date(2024, 1, 15),
            story="A wonderful day",
            location="Paris",
        )
        event = await create_event(db_session, event_data, "friend1")
        assert event.id is not None
        assert event.title == "Test Event"
        assert event.created_by == "friend1"

    @pytest.mark.asyncio
    async def test_get_event(self, db_session):
        """Test getting an event by ID."""
        event_data = EventCreate(
            title="Test Event",
            event_date=date(2024, 1, 15),
        )
        created = await create_event(db_session, event_data, "friend1")
        fetched = await get_event(db_session, created.id)
        assert fetched is not None
        assert fetched.id == created.id

    @pytest.mark.asyncio
    async def test_get_event_not_found(self, db_session):
        """Test getting a non-existent event."""
        result = await get_event(db_session, uuid4())
        assert result is None

    @pytest.mark.asyncio
    async def test_list_events(self, db_session):
        """Test listing events."""
        for i in range(5):
            event_data = EventCreate(
                title=f"Event {i}",
                event_date=date(2024, 1, i + 1),
            )
            await create_event(db_session, event_data, "friend1")

        events, total = await list_events(db_session, limit=3, offset=0)
        assert len(events) == 3
        assert total == 5
