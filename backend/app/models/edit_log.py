import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Index, ForeignKey
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class EditLog(Base):
    __tablename__ = "edit_logs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(10), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow
    )

    __table_args__ = (
        Index("idx_edit_logs_event_id", "event_id"),
        Index("idx_edit_logs_password_hash", "password_hash"),
    )
