from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ApplicationLogResponse(BaseModel):
    id: int
    application_id: int
    old_status: Optional[str]   # None for the very first log entry
    new_status: str
    changed_by: int             # user_id
    note: Optional[str]
    changed_at: datetime

    model_config = {"from_attributes": True}