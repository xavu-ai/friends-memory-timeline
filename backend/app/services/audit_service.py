from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog


async def create_audit_log(
    session: AsyncSession,
    event_id: Optional[UUID],
    friend_id: str,
    action: str,
    changes: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Create an audit log entry."""
    audit_log = AuditLog(
        event_id=event_id,
        friend_id=friend_id,
        action=action,
        changes=changes,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    session.add(audit_log)
    await session.commit()
    await session.refresh(audit_log)
    return audit_log
