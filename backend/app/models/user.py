from enum import Enum
from datetime import datetime
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class UserRole(str, Enum):
    STUDENT =  "student"
    COMPANY = "company"
    COORDINATOR = "coordinator"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    student: Mapped["Student"] = relationship("Student", back_populates="user")
    company: Mapped["Company"] = relationship("Company", back_populates="user")
    coordinator: Mapped["Coordinator"] = relationship("Coordinator", back_populates="user")
    