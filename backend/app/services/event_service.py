from datetime import date
from typing import Optional
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.event import Event
from app.models.audit_log import AuditLog
from app.schemas.event import EventCreate, EventUpdate


async def create_event(
    session: AsyncSession,
    event_data: EventCreate,
    created_by: str,
    photo_path: Optional[str] = None,
) -> Event:
    """Create a new event."""
    event = Event(
        title=event_data.title,
        event_date=event_data.event_date,
        story=event_data.story,
        location=event_data.location,
        photo_path=photo_path,
        created_by=created_by,
    )
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def get_event(session: AsyncSession, event_id: UUID) -> Optional[Event]:
    """Get a single event by ID (excluding soft-deleted)."""
    stmt = select(Event).where(Event.id == event_id, Event.deleted_at.is_(None))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def list_events(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> tuple[list[tuple[Event, int]], int]:
    """
    List events with edit count (no N+1 query).
    Returns tuple of (events with edit counts, total count).
    """
    # Base query for events with edit count
    count_stmt = select(func.count(Event.id)).where(Event.deleted_at.is_(None))
    if from_date:
        count_stmt = count_stmt.where(Event.event_date >= from_date)
    if to_date:
        count_stmt = count_stmt.where(Event.event_date <= to_date)

    total_result = await session.execute(count_stmt)
    total = total_result.scalar_one()

    # Query with edit count - no N+1
    stmt = (
        select(Event, func.count(AuditLog.id).label("edit_count"))
        .outerjoin(AuditLog, AuditLog.event_id == Event.id)
        .where(Event.deleted_at.is_(None))
        .group_by(Event.id)
        .order_by(Event.event_date.desc())
        .limit(limit)
        .offset(offset)
    )
    if from_date:
        stmt = stmt.where(Event.event_date >= from_date)
    if to_date:
        stmt = stmt.where(Event.event_date <= to_date)

    result = await session.execute(stmt)
    events_with_counts = result.all()

    return events_with_counts, total


async def update_event(
    session: AsyncSession,
    event: Event,
    event_data: EventUpdate,
    photo_path: Optional[str] = None,
) -> Event:
    """Update an existing event."""
    update_data = event_data.model_dump(exclude_unset=True)
    if photo_path is not None:
        update_data["photo_path"] = photo_path

    for key, value in update_data.items():
        setattr(event, key, value)

    await session.commit()
    await session.refresh(event)
    return event


async def soft_delete_event(session: AsyncSession, event: Event) -> Event:
    """Soft delete an event."""
    from datetime import datetime, timezone
    event.deleted_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(event)
    return event
