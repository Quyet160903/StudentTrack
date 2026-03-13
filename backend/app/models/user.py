from enum import Enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class UserRole(str, Enum):
    STUDENT     = "student"
    COMPANY     = "company"
    COORDINATOR = "coordinator"


class User(Base):
    __tablename__ = "users"

    id:            Mapped[int]      = mapped_column(primary_key=True, index=True)
    email:         Mapped[str]      = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str]      = mapped_column(String(255), nullable=False)
    role:          Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False)  # ← fix: SQLEnum(UserRole)
    is_active:     Mapped[bool]     = mapped_column(default=True)
    created_at:    Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at:    Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    student:     Mapped[Optional["Student"]]     = relationship("Student",     back_populates="user", uselist=False)
    company:     Mapped[Optional["Company"]]     = relationship("Company",     back_populates="user", uselist=False)
    coordinator: Mapped[Optional["Coordinator"]] = relationship("Coordinator", back_populates="user", uselist=False)

    @property
    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT

    @property
    def is_company(self) -> bool:
        return self.role == UserRole.COMPANY

    @property
    def is_coordinator(self) -> bool:
        return self.role == UserRole.COORDINATOR