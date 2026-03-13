from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate, JobApprovalAction, JobResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse
from app.services.job_service import JobService
from app.core.deps import require_company, require_coordinator

job_router = APIRouter(prefix="/jobs", tags=["jobs"])


# ── Public ─────────────────────────────────────────────────────────────────────

@job_router.get("/", response_model=PaginatedResponse[JobResponse])
def get_all_jobs(
    db: Session = Depends(get_db),
    params: PaginationParams = Depends(),   # FastAPI reads ?page= & ?page_size= automatically
):
    """
    All open jobs — visible to everyone.

    Query params:
        ?page=1&page_size=10
    """
    return JobService.get_all(db, params)


# ── Coordinator ─────────────────────────────────────────────────────────────
# IMPORTANT: /all, /pending, /my must stay BEFORE /{job_id}

@job_router.get("/all", response_model=PaginatedResponse[JobResponse])
def get_all_jobs_coordinator(
    db: Session = Depends(get_db),
    params: PaginationParams = Depends(),
    current_user: User = Depends(require_coordinator),
):
    """Coordinator — all jobs regardless of status, paginated."""
    return JobService.get_all_for_coordinator(db, params)


@job_router.get("/pending", response_model=PaginatedResponse[JobResponse])
def get_pending_jobs(
    db: Session = Depends(get_db),
    params: PaginationParams = Depends(),
    current_user: User = Depends(require_coordinator),
):
    """Coordinator — pending approval queue, paginated."""
    return JobService.get_pending(db, params)


@job_router.put("/{job_id}/approve", response_model=JobResponse)
def approve_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_coordinator),
):
    return JobService.approve(db, job_id, current_user)


@job_router.put("/{job_id}/reject", response_model=JobResponse)
def reject_job(
    job_id: int,
    request: JobApprovalAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_coordinator),
):
    return JobService.reject(db, job_id, request, current_user)


# ── Company ────────────────────────────────────────────────────────────────────

@job_router.get("/my", response_model=PaginatedResponse[JobResponse])
def get_my_jobs(
    db: Session = Depends(get_db),
    params: PaginationParams = Depends(),
    current_user: User = Depends(require_company),
):
    """Company — their own jobs (all statuses), paginated."""
    return JobService.get_by_company(db, current_user, params)


@job_router.post("/", response_model=JobResponse)
def create_job(
    request: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company),
):
    return JobService.create(db, request, current_user)


@job_router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    request: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company),
):
    return JobService.update(db, job_id, request, current_user)


@job_router.post("/{job_id}/resubmit", response_model=JobResponse)
def resubmit_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company),
):
    return JobService.resubmit(db, job_id, current_user)


@job_router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company),
):
    return JobService.delete(db, job_id, current_user)


# ── Public detail — must be LAST ───────────────────────────────────────────────

@job_router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return JobService.get_by_id(db, job_id)