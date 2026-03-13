from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Coordinator(Base):
    __tablename__ = "coordinators"

    id:         Mapped[int]           = mapped_column(primary_key=True, index=True)
    user_id:    Mapped[int]           = mapped_column(ForeignKey("users.id"), nullable=False)
    full_name:  Mapped[str]           = mapped_column(String(255), nullable=False)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone:      Mapped[Optional[str]] = mapped_column(String(20),  nullable=True)
    created_at: Mapped[datetime]      = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime]      = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="coordinator")