import pytest
from datetime import date
from uuid import uuid4
from app.services.event_service import create_event, get_event, list_events, update_event, delete_event
from app.schemas.event import EventCreate, EventUpdate
from app.models.edit_log import EditLog
from sqlalchemy import select


class TestEventService:
    @pytest.mark.asyncio
    async def test_create_event(self, db_session):
        """Test creating an event."""
        event_data = EventCreate(
            title="Test Event",
            date=date(2024, 1, 15),
            story="A wonderful day",
            location="Paris",
        )
        event = await create_event(db_session, event_data, "test_hash")
        assert event.id is not None
        assert event.title == "Test Event"
        assert event.date == date(2024, 1, 15)

    @pytest.mark.asyncio
    async def test_create_event_logs_to_edit_logs(self, db_session):
        """Test that creating an event adds an edit log."""
        event_data = EventCreate(title="Test", date=date(2024, 1, 1))
        event = await create_event(db_session, event_data, "hash123")

        result = await db_session.execute(
            select(EditLog).where(EditLog.event_id == event.id)
        )
        log = result.scalar_one()
        assert log.password_hash == "hash123"
        assert log.action == "create"

    @pytest.mark.asyncio
    async def test_get_event(self, db_session):
        """Test getting an event by ID."""
        event_data = EventCreate(title="Test Event", date=date(2024, 1, 15))
        created = await create_event(db_session, event_data, "hash")
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
        """Test listing events returns newest first."""
        for i in range(5):
            event_data = EventCreate(
                title=f"Event {i}",
                date=date(2024, 1, i + 1),
            )
            await create_event(db_session, event_data, "hash")

        events, total = await list_events(db_session, limit=3, offset=0)
        assert len(events) == 3
        assert total == 5
        assert events[0].title == "Event 4"

    @pytest.mark.asyncio
    async def test_update_event(self, db_session):
        """Test updating an event."""
        event_data = EventCreate(title="Original", date=date(2024, 1, 1))
        event = await create_event(db_session, event_data, "hash")

        update_data = EventUpdate(title="Updated")
        updated = await update_event(db_session, event, update_data, "hash2")
        assert updated.title == "Updated"

    @pytest.mark.asyncio
    async def test_delete_event(self, db_session):
        """Test deleting an event."""
        event_data = EventCreate(title="To Delete", date=date(2024, 1, 1))
        event = await create_event(db_session, event_data, "hash")

        await delete_event(db_session, event, "hash2")

        fetched = await get_event(db_session, event.id)
        assert fetched is None
