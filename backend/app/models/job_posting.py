import enum
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from app.db.database import Base


class JobType(str, enum.Enum):
    INTERNSHIP = "internship"
    FULL_TIME  = "full_time"
    PART_TIME  = "part_time"


class JobStatus(str, enum.Enum):
    PENDING  = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    OPEN     = "open"
    CLOSED   = "closed"
    DRAFT    = "draft"


class JobPosting(Base):
    __tablename__ = "job_postings"

    id:           Mapped[int]      = mapped_column(primary_key=True, index=True)
    company_id:   Mapped[int]      = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    title:        Mapped[str]      = mapped_column(String(255), nullable=False)
    description:  Mapped[str]      = mapped_column(Text, nullable=True)
    requirements: Mapped[str]      = mapped_column(Text, nullable=True)
    location:     Mapped[str]      = mapped_column(String(255), nullable=True)
    job_type: Mapped[JobType]   = mapped_column(SQLEnum(JobType,   values_callable=lambda x: [e.value for e in x]), nullable=False)
    salary_min:   Mapped[float]    = mapped_column(Numeric(10, 2), nullable=True)
    salary_max:   Mapped[float]    = mapped_column(Numeric(10, 2), nullable=True)
    status:   Mapped[JobStatus] = mapped_column(SQLEnum(JobStatus, values_callable=lambda x: [e.value for e in x]), nullable=False, default=JobStatus.PENDING)
    deadline:     Mapped[datetime] = mapped_column(nullable=True)
    rejection_note: Mapped[str]    = mapped_column(nullable=True)
    created_at:   Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at:   Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    company:      Mapped["Company"]            = relationship("Company", back_populates="job_postings")
    applications: Mapped[list["Application"]]  = relationship("Application", back_populates="job", cascade="all, delete-orphan")