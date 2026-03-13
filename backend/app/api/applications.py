from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.application import ApplicationResponse, ApplicationCreate, ApplicationUpdate

from app.models.user import User

from app.core.deps import require_student, require_company, require_coordinator, get_current_user
from app.db.database import get_db

from app.services.application_service import ApplicationService

application_router = APIRouter(prefix="/applications", tags=["applications"])

@application_router.post("/", response_model=ApplicationResponse)
def apply(request: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(require_student)):
    return ApplicationService.apply(db, request, current_user)

@application_router.get("/all", response_model=List[ApplicationResponse])
def get_all_applications(db: Session = Depends(get_db), 
                         current_user: User = Depends(require_coordinator)):
    return ApplicationService.get_all(db)

@application_router.get("/my", response_model=List[ApplicationResponse])
def get_my_applications(db: Session = Depends(get_db), current_user: User = Depends(require_student)):
    return ApplicationService.get_my_applications(db, current_user)

@application_router.get("/job/{job_id}", response_model=List[ApplicationResponse])
def get_job_applications(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_company)):
    return ApplicationService.get_job_applications(db, job_id, current_user)

@application_router.put("/{app_id}/status", response_model=ApplicationResponse)
def update_status(app_id: int, request: ApplicationUpdate, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApplicationService.update_status(db, app_id, request, current_user)