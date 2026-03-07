from enum import Enum
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class JobType(str, Enum):
    INTERNSHIP = "internship"
    FULL_TIME = "full_time"
    PART_TIME = "part_time"

class JobStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"

class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    requirements: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(255))
    job_type: Mapped[JobType] = mapped_column(SQLEnum(JobType), nullable=False)
    salary_min: Mapped[float] = mapped_column(Numeric(10, 2))
    salary_max: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[JobStatus] = mapped_column(SQLEnum(JobStatus), default=JobStatus.DRAFT)
    deadline: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    company: Mapped["Company"] = relationship("Company", back_populates="job_postings")
    applications: Mapped[list["Application"]] = relationship("Application", back_populates="job")