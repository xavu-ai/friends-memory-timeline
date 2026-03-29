from datetime import date
from typing import Optional
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import Event
from app.models.edit_log import EditLog
from app.schemas.event import EventCreate, EventUpdate


async def create_event(
    session: AsyncSession,
    event_data: EventCreate,
    password_hash: str,
) -> Event:
    """Create a new event and log the creation."""
    event = Event(
        date=event_data.date,
        title=event_data.title,
        story=event_data.story,
        photo_url=event_data.photo_url,
        location=event_data.location,
    )
    session.add(event)
    await session.flush()

    edit_log = EditLog(
        event_id=event.id,
        password_hash=password_hash,
        action="create",
    )
    session.add(edit_log)

    await session.commit()
    await session.refresh(event)
    return event


async def get_event(session: AsyncSession, event_id: UUID) -> Optional[Event]:
    """Get a single event by ID."""
    stmt = select(Event).where(Event.id == event_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def list_events(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Event], int]:
    """List events (newest first) with total count."""
    total_stmt = select(func.count(Event.id))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()

    stmt = (
        select(Event)
        .order_by(Event.date.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    events = list(result.scalars().all())

    return events, total


async def update_event(
    session: AsyncSession,
    event: Event,
    event_data: EventUpdate,
    password_hash: str,
) -> Event:
    """Update an existing event and log the change."""
    update_data = event_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)

    edit_log = EditLog(
        event_id=event.id,
        password_hash=password_hash,
        action="update",
    )
    session.add(edit_log)

    await session.commit()
    await session.refresh(event)
    return event


async def delete_event(
    session: AsyncSession,
    event: Event,
    password_hash: str,
) -> None:
    """Delete an event and log the deletion."""
    edit_log = EditLog(
        event_id=event.id,
        password_hash=password_hash,
        action="delete",
    )
    session.add(edit_log)
    await session.delete(event)
    await session.commit()
