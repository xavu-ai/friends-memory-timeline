import os
import uuid
import shutil
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.event import EventCreate, EventUpdate, EventResponse, EventListResponse
from app.services.event_service import create_event, get_event, list_events, update_event, soft_delete_event
from app.services.audit_service import create_audit_log
from app.dependencies import get_current_friend
from app.config import settings

router = APIRouter(prefix="/api/v1/events", tags=["events"])


def get_client_ip(request: Request) -> str:
    """Extract client IP from request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("", status_code=201, response_model=EventResponse)
async def create_event_endpoint(
    request: Request,
    title: str = Form(...),
    date: date = Form(...),
    story: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_friend: str = Depends(get_current_friend),
) -> EventResponse:
    """Create a new event."""
    photo_path = None
    if photo:
        if photo.size and photo.size > settings.max_upload_size:
            raise HTTPException(413, detail="File too large")
        os.makedirs(settings.upload_dir, exist_ok=True)
        ext = os.path.splitext(photo.filename)[1] if photo.filename else ".jpg"
        photo_path = os.path.join(settings.upload_dir, f"{uuid.uuid4()}{ext}")
        with open(photo_path, "wb") as f:
            shutil.copyfileobj(photo.file, f)
        photo_path = photo_path

    event_data = EventCreate(title=title, event_date=date, story=story, location=location)
    event = await create_event(db, event_data, current_friend, photo_path)

    await create_audit_log(
        db,
        event_id=event.id,
        friend_id=current_friend,
        action="CREATE",
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("User-Agent"),
    )

    return EventResponse.model_validate(event)


@router.get("", response_model=EventListResponse)
async def list_events_endpoint(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_friend: str = Depends(get_current_friend),
) -> EventListResponse:
    """List events (newest first)."""
    events_with_counts, total = await list_events(db, limit, offset, from_date, to_date)
    items = [EventResponse.model_validate(e) for e, _ in events_with_counts]
    return EventListResponse(items=items, total=total)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_endpoint(
    event_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_friend: str = Depends(get_current_friend),
) -> EventResponse:
    """Get a single event by ID."""
    event = await get_event(db, event_id)
    if not event:
        raise HTTPException(404, detail="Event not found")
    return EventResponse.model_validate(event)


@router.put("/{event_id}", response_model=EventResponse)
async def update_event_endpoint(
    request: Request,
    event_id: uuid.UUID,
    title: Optional[str] = Form(None),
    date: Optional[date] = Form(None),
    story: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_friend: str = Depends(get_current_friend),
) -> EventResponse:
    """Update an existing event."""
    event = await get_event(db, event_id)
    if not event:
        raise HTTPException(404, detail="Event not found")

    photo_path = None
    if photo:
        if photo.size and photo.size > settings.max_upload_size:
            raise HTTPException(413, detail="File too large")
        os.makedirs(settings.upload_dir, exist_ok=True)
        ext = os.path.splitext(photo.filename)[1] if photo.filename else ".jpg"
        photo_path = os.path.join(settings.upload_dir, f"{uuid.uuid4()}{ext}")
        with open(photo_path, "wb") as f:
            shutil.copyfileobj(photo.file, f)

    old_values = {
        "title": event.title,
        "event_date": event.event_date.isoformat(),
        "story": event.story,
        "location": event.location,
    }

    event_data = EventUpdate(title=title, event_date=date, story=story, location=location)
    updated_event = await update_event(db, event, event_data, photo_path)

    new_values = {
        "title": updated_event.title,
        "event_date": updated_event.event_date.isoformat(),
        "story": updated_event.story,
        "location": updated_event.location,
    }

    await create_audit_log(
        db,
        event_id=event_id,
        friend_id=current_friend,
        action="UPDATE",
        changes={"old": old_values, "new": new_values},
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("User-Agent"),
    )

    return EventResponse.model_validate(updated_event)


@router.delete("/{event_id}")
async def delete_event_endpoint(
    request: Request,
    event_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_friend: str = Depends(get_current_friend),
) -> dict[str, bool]:
    """Soft delete an event."""
    event = await get_event(db, event_id)
    if not event:
        raise HTTPException(404, detail="Event not found")

    await soft_delete_event(db, event)

    await create_audit_log(
        db,
        event_id=event_id,
        friend_id=current_friend,
        action="DELETE",
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("User-Agent"),
    )

    return {"deleted": True}
