"""
app/schemas/application_log.py
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ApplicationLogResponse(BaseModel):
    id: int
    application_id: int
    old_status: Optional[str]
    new_status: str
    changed_by: int
    changed_by_name: Optional[str]
    changed_by_role: Optional[str]
    note: Optional[str]
    changed_at: datetime

    model_config = {"from_attributes": False}  # manual construction, not ORM direct