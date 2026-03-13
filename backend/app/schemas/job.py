from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from app.models.job_posting import JobType, JobStatus


class JobCreate(BaseModel):
    title: str
    description: str | None = None
    requirements: str | None = None
    location: str | None = None
    job_type: JobType
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    deadline: datetime | None = None


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    requirements: str | None = None
    location: str | None = None
    job_type: JobType | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    status: JobStatus | None = None
    deadline: datetime | None = None


class JobApprovalAction(BaseModel):
    note: str | None = None


class JobResponse(BaseModel):
    id: int
    company_id: int
    title: str
    description: str | None = None
    requirements: str | None = None
    location: str | None = None
    job_type: JobType
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    status: JobStatus
    deadline: datetime | None = None
    rejection_note: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
