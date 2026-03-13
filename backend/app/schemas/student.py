from pydantic import BaseModel
from typing import Optional

class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    student_id: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[float] = None
    phone: Optional[str] = None
    graduation_year: Optional[int] = None
    resume_url: Optional[str] = None
    bio: Optional[str] = None

class StudentResponse(BaseModel):
    id: int
    user_id: int
    full_name: Optional[str] = None
    student_id: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[float] = None
    phone: Optional[str] = None
    graduation_year: Optional[int] = None
    resume_url: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True