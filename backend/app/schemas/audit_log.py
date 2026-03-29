from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class AuditLogBase(BaseModel):
    event_id: Optional[UUID] = None
    friend_id: str
    action: str
    changes: Optional[dict] = None


class AuditLogResponse(AuditLogBase):
    id: UUID
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogListResponse(BaseModel):
    logs: list[AuditLogResponse]
