from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.student import StudentResponse, StudentUpdate
from app.services.student_service import StudentService
from app.core.deps import require_coordinator, require_student

student_router = APIRouter(prefix="/students", tags=["students"])

@student_router.get("/", response_model=List[StudentResponse])
def get_all(db: Session = Depends(get_db), current_user: User = Depends(require_coordinator)):
    return StudentService.get_all(db)

@student_router.get("/profile", response_model=StudentResponse)
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(require_student)):
    return StudentService.get_profile(db, current_user)

@student_router.put("/profile", response_model=StudentResponse)
def update_profile(request: StudentUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_student)):
    return StudentService.update_profile(db, request, current_user)