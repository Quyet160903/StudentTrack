from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id:            Mapped[int]           = mapped_column(primary_key=True, index=True)
    user_id:       Mapped[int]           = mapped_column(ForeignKey("users.id"), nullable=False)
    name:          Mapped[str]           = mapped_column(String(255), nullable=False)
    description:   Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    website:       Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location:      Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20),  nullable=True)
    logo_url:      Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at:    Mapped[datetime]      = mapped_column(default=datetime.utcnow)
    updated_at:    Mapped[datetime]      = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user:         Mapped["User"]              = relationship("User",       back_populates="company")
    job_postings: Mapped[list["JobPosting"]]  = relationship("JobPosting", back_populates="company")