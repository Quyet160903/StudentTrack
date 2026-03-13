from datetime import datetime
from pydantic import BaseModel

from app.models.application import ApplicationStatus

class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: str | None = None
    resume_url: str | None = None

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus
    note: str | None = None

class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    job_id: int
    status: ApplicationStatus
    cover_letter: str | None
    resume_url: str | None
    applied_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True