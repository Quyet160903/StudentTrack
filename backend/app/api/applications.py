from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.application import ApplicationResponse, ApplicationCreate, ApplicationUpdate
from app.schemas.application_log import ApplicationLogResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse
from app.models.user import User
from app.core.deps import require_student, require_company, require_coordinator, get_current_user
from app.db.database import get_db
from app.services.application_service import ApplicationService

application_router = APIRouter(prefix="/applications", tags=["applications"])


@application_router.post("/", response_model=ApplicationResponse)
def apply(
    request: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student)
):
    return ApplicationService.create(db, request, current_user)


# ── IMPORTANT: /all and /my must be BEFORE /{app_id} ──────────────────────────

@application_router.get("/all", response_model=PaginatedResponse[ApplicationResponse])
def get_all_applications(
    db: Session = Depends(get_db),
    params: PaginationParams = Depends(),
    status: str | None = Query(default=None, description="Filter by status, e.g. accepted"),
    current_user: User = Depends(require_coordinator)
):
    """
    Coordinator — all applications, paginated, with optional status filter.

    GET /applications/all?page=1&page_size=15
    GET /applications/all?page=1&page_size=15&status=accepted
    """
    from app.models.application import ApplicationStatus
    try:
        status_enum = ApplicationStatus(status) if status else None
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=f"Invalid status: {status}")
    return ApplicationService.get_all(db, params, status_enum)


@application_router.get("/my", response_model=List[ApplicationResponse])
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student)
):
    """Student — their own applications (no pagination needed, usually small list)."""
    return ApplicationService.get_my_applications(db, current_user)


@application_router.get("/job/{job_id}", response_model=List[ApplicationResponse])
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company)
):
    """Company — all applicants for one of their jobs."""
    return ApplicationService.get_by_job(db, job_id, current_user)


@application_router.get("/{app_id}/logs", response_model=List[ApplicationLogResponse])
def get_application_logs(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Status change history for one application.
    Accessible by the student who applied, the company that owns the job, or coordinator.
    """
    return ApplicationService.get_logs(db, app_id, current_user)


@application_router.put("/{app_id}/status", response_model=ApplicationResponse)
def update_status(
    app_id: int,
    request: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update application status.
    - Student: withdraw only (status=withdrawn)
    - Company: reviewing / interview / accepted / rejected (own jobs only)
    - Coordinator: any status
    """
    return ApplicationService.update_status(db, app_id, request, current_user)