from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventListResponse,
)
from app.services.event_service import (
    create_event,
    get_event,
    list_events,
    update_event,
    delete_event,
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.get("", response_model=EventListResponse)
async def list_events_endpoint(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(get_current_user),
) -> EventListResponse:
    """List events (newest first)."""
    events, total = await list_events(db, limit=limit, offset=offset)
    return EventListResponse(
        events=[EventResponse.model_validate(e) for e in events],
        total=total,
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_endpoint(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(get_current_user),
) -> EventResponse:
    """Get a single event by ID."""
    event = await get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse.model_validate(event)


@router.post("", status_code=201, response_model=EventResponse)
async def create_event_endpoint(
    event_data: EventCreate,
    db: AsyncSession = Depends(get_db),
    password_hash: str = Depends(get_current_user),
) -> EventResponse:
    """Create a new event."""
    try:
        event = await create_event(db, event_data, password_hash)
        return EventResponse.model_validate(event)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create event")


@router.put("/{event_id}", response_model=EventResponse)
async def update_event_endpoint(
    event_id: UUID,
    event_data: EventUpdate,
    db: AsyncSession = Depends(get_db),
    password_hash: str = Depends(get_current_user),
) -> EventResponse:
    """Update an existing event."""
    event = await get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    try:
        updated = await update_event(db, event, event_data, password_hash)
        return EventResponse.model_validate(updated)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update event")


@router.delete("/{event_id}", status_code=204)
async def delete_event_endpoint(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    password_hash: str = Depends(get_current_user),
) -> None:
    """Delete an event."""
    event = await get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    try:
        await delete_event(db, event, password_hash)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete event")
