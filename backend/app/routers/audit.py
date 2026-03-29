from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogListResponse
from app.dependencies import get_current_friend

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.get("/{event_id}/audit", response_model=AuditLogListResponse)
async def get_event_audit_trail(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_friend: str = Depends(get_current_friend),
) -> AuditLogListResponse:
    """Get audit trail for a specific event."""
    stmt = select(AuditLog).where(AuditLog.event_id == event_id).order_by(AuditLog.created_at.desc())
    result = await db.execute(stmt)
    logs = result.scalars().all()
    return AuditLogListResponse(logs=list(logs))
