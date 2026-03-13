from datetime import datetime
from typing import Optional

from sqlalchemy import Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.application import ApplicationStatus


class ApplicationStatusLog(Base):
    __tablename__ = "application_status_logs"

    id:             Mapped[int]                      = mapped_column(primary_key=True, index=True)
    application_id: Mapped[int]                      = mapped_column(ForeignKey("applications.id"), nullable=False)
    old_status: Mapped[Optional[ApplicationStatus]] = mapped_column(SQLEnum(ApplicationStatus, values_callable=lambda x: [e.value for e in x]), nullable=True)
    new_status: Mapped[ApplicationStatus]           = mapped_column(SQLEnum(ApplicationStatus, values_callable=lambda x: [e.value for e in x]), nullable=False)
    changed_by:     Mapped[int]                      = mapped_column(ForeignKey("users.id"),        nullable=False)
    note:           Mapped[Optional[str]]            = mapped_column(Text, nullable=True)
    changed_at:     Mapped[datetime]                 = mapped_column(default=datetime.utcnow)

    application:      Mapped["Application"] = relationship("Application", back_populates="status_logs")
    changed_by_user:  Mapped["User"]        = relationship("User")