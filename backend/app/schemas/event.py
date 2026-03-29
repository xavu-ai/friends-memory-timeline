from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    date: date
    title: str = Field(..., max_length=255)
    story: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=255)


class EventUpdate(BaseModel):
    date: Optional[date] = None
    title: Optional[str] = Field(None, max_length=255)
    story: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=255)


class EventResponse(BaseModel):
    id: UUID
    date: date
    title: str
    story: Optional[str] = None
    photo_url: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    events: list[EventResponse]
    total: int
