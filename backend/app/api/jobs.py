from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.job import JobResponse, JobCreate, JobUpdate, JobApprovalAction
from app.models.user import User
from app.services.job_service import JobService
from app.db.database import get_db
from app.core.deps import require_company, require_coordinator

job_router = APIRouter(prefix="/jobs", tags=["jobs"])

@job_router.get("/", response_model=List[JobResponse])
def get_all(db: Session = Depends(get_db)):
    return JobService.get_all(db)

@job_router.get("/my", response_model=List[JobResponse])
def get_my_jobs(db: Session = Depends(get_db), 
                current_user: User = Depends(require_company)):
    return JobService.get_by_company(db, current_user)

@job_router.get("/all", response_model=List[JobResponse])
def get_all_jobs_coordinator(db: Session = Depends(get_db),
                             current_user: User = Depends(require_coordinator)):
    return JobService.get_all_for_coordinator(db)

@job_router.get("/pending", response_model=List[JobResponse])
def get_pending_jobs(db: Session = Depends(get_db),
                     current_user: User = Depends(require_coordinator)):
    return JobService.get_pending(db)

@job_router.get("/{job_id}", response_model=JobResponse)
def get_by_id(job_id: int, db: Session = Depends(get_db)):
    return JobService.get_by_id(db, job_id)

@job_router.post("/", response_model=JobResponse)
def create(request: JobCreate, db: Session = Depends(get_db), current_user: User = Depends(require_company)):
    return JobService.create(db, request, current_user)

@job_router.put("/{job_id}", response_model=JobResponse)
def update(job_id: int, request: JobUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_company)):
    return JobService.update(db, job_id, request, current_user)

@job_router.delete("/{job_id}")
def delete(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_company)) -> dict:
    return JobService.delete(db, job_id, current_user)

@job_router.put("/{job_id}/approve", response_model=JobResponse)
def approve_job(job_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(require_coordinator)):
    return JobService.approve(db, job_id, current_user)

@job_router.put("/{job_id}/reject", response_model=JobResponse)
def reject_job(job_id: int, request: JobApprovalAction,
               db: Session = Depends(get_db),
               current_user: User = Depends(require_coordinator)):
    return JobService.reject(db, job_id, request, current_user)