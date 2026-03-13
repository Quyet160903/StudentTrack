from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Student(Base):
    __tablename__ = "students"

    id:              Mapped[int]            = mapped_column(primary_key=True, index=True)
    user_id:         Mapped[int]            = mapped_column(ForeignKey("users.id"), nullable=False)
    student_id:      Mapped[Optional[str]]  = mapped_column(String(20),  nullable=True)
    full_name:       Mapped[Optional[str]]  = mapped_column(String(255), nullable=True)
    major:           Mapped[Optional[str]]  = mapped_column(String(100), nullable=True)
    gpa:             Mapped[Optional[float]] = mapped_column(nullable=True)
    phone:           Mapped[Optional[str]]  = mapped_column(String(20),  nullable=True)
    graduation_year: Mapped[Optional[int]]  = mapped_column(nullable=True)
    resume_url:      Mapped[Optional[str]]  = mapped_column(String(500), nullable=True)
    bio:             Mapped[Optional[str]]  = mapped_column(Text,        nullable=True)
    created_at:      Mapped[datetime]       = mapped_column(default=datetime.utcnow)
    updated_at:      Mapped[datetime]       = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user:         Mapped["User"]               = relationship("User",        back_populates="student")
    applications: Mapped[list["Application"]]  = relationship("Application", back_populates="student")