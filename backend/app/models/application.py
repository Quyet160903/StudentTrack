from enum import Enum
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ApplicationStatus(str, Enum):
    PENDING   = "pending"
    REVIEWING = "reviewing"
    INTERVIEW = "interview"
    ACCEPTED  = "accepted"
    REJECTED  = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    __tablename__ = "applications"

    id:           Mapped[int]               = mapped_column(primary_key=True, index=True)
    student_id:   Mapped[int]               = mapped_column(ForeignKey("students.id"),     nullable=False, index=True)
    job_id:       Mapped[int]               = mapped_column(ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[ApplicationStatus] = mapped_column(SQLEnum(ApplicationStatus, values_callable=lambda x: [e.value for e in x]), default=ApplicationStatus.PENDING)
    cover_letter: Mapped[Optional[str]]     = mapped_column(Text,        nullable=True)
    resume_url:   Mapped[Optional[str]]     = mapped_column(String(500), nullable=True)
    applied_at:   Mapped[datetime]          = mapped_column(default=datetime.utcnow)
    updated_at:   Mapped[datetime]          = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    student:     Mapped["Student"]                   = relationship("Student",              back_populates="applications")
    job:         Mapped["JobPosting"]                = relationship("JobPosting",            back_populates="applications")
    status_logs: Mapped[list["ApplicationStatusLog"]] = relationship("ApplicationStatusLog", back_populates="application")