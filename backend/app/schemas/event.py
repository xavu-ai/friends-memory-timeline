from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, AliasPath, ConfigDict


class EventBase(BaseModel):
    title: str = Field(..., max_length=255)
    event_date: date
    story: Optional[str] = None
    location: Optional[str] = Field(None, max_length=255)


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    event_date: Optional[date] = None
    story: Optional[str] = None
    location: Optional[str] = Field(None, max_length=255)


class EventResponse(EventBase):
    id: UUID
    photo_path: Optional[str] = None
    metadata: dict = Field(default={}, validation_alias=AliasPath("extra_metadata"))
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class EventListResponse(BaseModel):
    items: list[EventResponse]
    total: int
