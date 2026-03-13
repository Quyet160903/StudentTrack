from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Tuple

from app.models.user import User
from app.models.company import Company
from app.models.job_posting import JobPosting, JobStatus
from app.schemas.job import JobCreate, JobUpdate, JobApprovalAction, JobResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse


class JobService:

    @staticmethod
    def create(db: Session, request: JobCreate, current_user: User) -> JobResponse:
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company profile not found")

        job = JobPosting(
            company_id=company.id,
            title=request.title,
            description=request.description,
            requirements=request.requirements,
            location=request.location,
            job_type=request.job_type,
            salary_min=request.salary_min,
            salary_max=request.salary_max,
            deadline=request.deadline,
            status=JobStatus.PENDING,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return JobResponse.model_validate(job)

    @staticmethod
    def get_all(db: Session, params: PaginationParams) -> PaginatedResponse[JobResponse]:
        """Public — only OPEN jobs, paginated."""
        # Step 1: build the base query (reused for both COUNT and data fetch)
        query = db.query(JobPosting).filter(JobPosting.status == JobStatus.OPEN)

        # Step 2: COUNT total matching rows (before applying LIMIT/OFFSET)
        # This is what goes into total_pages calculation
        total = query.count()

        # Step 3: fetch only the rows for this page
        # .offset() skips rows, .limit() takes only page_size rows
        jobs = query.order_by(JobPosting.id.desc()).offset(params.offset).limit(params.page_size).all()

        return PaginatedResponse.create(
            items=[JobResponse.model_validate(j) for j in jobs],
            total=total,
            params=params,
        )

    @staticmethod
    def get_all_for_coordinator(db: Session, params: PaginationParams) -> PaginatedResponse[JobResponse]:
        """Coordinator — all jobs regardless of status, paginated."""
        query = db.query(JobPosting)
        total = query.count()
        jobs = query.order_by(JobPosting.id.desc()).offset(params.offset).limit(params.page_size).all()
        return PaginatedResponse.create(
            items=[JobResponse.model_validate(j) for j in jobs],
            total=total,
            params=params,
        )

    @staticmethod
    def get_pending(db: Session, params: PaginationParams) -> PaginatedResponse[JobResponse]:
        """Coordinator — pending approval queue, paginated."""
        query = db.query(JobPosting).filter(JobPosting.status == JobStatus.PENDING)
        total = query.count()
        jobs = query.order_by(JobPosting.id.asc()).offset(params.offset).limit(params.page_size).all()
        return PaginatedResponse.create(
            items=[JobResponse.model_validate(j) for j in jobs],
            total=total,
            params=params,
        )

    @staticmethod
    def get_by_company(db: Session, current_user: User, params: PaginationParams) -> PaginatedResponse[JobResponse]:
        """Company — their own jobs (all statuses), paginated."""
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company profile not found")
        query = db.query(JobPosting).filter(JobPosting.company_id == company.id)
        total = query.count()
        jobs = query.order_by(JobPosting.id.desc()).offset(params.offset).limit(params.page_size).all()
        return PaginatedResponse.create(
            items=[JobResponse.model_validate(j) for j in jobs],
            total=total,
            params=params,
        )

    @staticmethod
    def get_by_id(db: Session, job_id: int) -> JobResponse:
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return JobResponse.model_validate(job)

    @staticmethod
    def update(db: Session, job_id: int, request: JobUpdate, current_user: User) -> JobResponse:
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.company_id != company.id:
            raise HTTPException(status_code=403, detail="You can only update your own jobs")

        update_data = request.model_dump(exclude_none=True)
        new_status = update_data.pop("status", None)

        # ── Case 1: pure status change (no content edits) ──────────────────
        if new_status is not None and not update_data:
            allowed_transitions = {
                JobStatus.APPROVED: [JobStatus.OPEN],
                JobStatus.OPEN:     [JobStatus.CLOSED],
                JobStatus.CLOSED:   [JobStatus.OPEN],   # reopen without re-approval
            }
            allowed = allowed_transitions.get(job.status, [])
            if new_status not in allowed:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot change status from '{job.status.value}' to '{new_status.value}'"
                )
            job.status = new_status

        # ── Case 2: content edits (with or without status) ─────────────────
        elif update_data:
            # editing content on a live/closed job → reset to PENDING for re-approval
            if job.status in (JobStatus.OPEN, JobStatus.CLOSED):
                job.status = JobStatus.PENDING
            # editing a PENDING or REJECTED job → stay as-is (or PENDING after resubmit)
            for field, value in update_data.items():
                setattr(job, field, value)

        db.commit()
        db.refresh(job)
        return JobResponse.model_validate(job)

    @staticmethod
    def resubmit(db: Session, job_id: int, current_user: User) -> JobResponse:
        """Company resubmits a rejected job for re-approval."""
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.company_id != company.id:
            raise HTTPException(status_code=403, detail="Not your job")
        if job.status != JobStatus.REJECTED:
            raise HTTPException(status_code=400, detail="Only rejected jobs can be resubmitted")

        job.status = JobStatus.PENDING
        job.rejection_note = None
        db.commit()
        db.refresh(job)
        return JobResponse.model_validate(job)

    @staticmethod
    def approve(db: Session, job_id: int, current_user: User) -> JobResponse:
        """Coordinator approves a pending job."""
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.status != JobStatus.PENDING:
            raise HTTPException(status_code=400, detail="Only pending jobs can be approved")

        job.status = JobStatus.APPROVED
        job.rejection_note = None
        db.commit()
        db.refresh(job)
        return JobResponse.model_validate(job)

    @staticmethod
    def reject(db: Session, job_id: int, request: JobApprovalAction, current_user: User) -> JobResponse:
        """Coordinator rejects a pending job with an optional note."""
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.status != JobStatus.PENDING:
            raise HTTPException(status_code=400, detail="Only pending jobs can be rejected")

        job.status = JobStatus.REJECTED
        job.rejection_note = request.note
        db.commit()
        db.refresh(job)
        return JobResponse.model_validate(job)

    @staticmethod
    def delete(db: Session, job_id: int, current_user: User) -> dict:
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.company_id != company.id:
            raise HTTPException(status_code=403, detail="You can only delete your own jobs")
        db.delete(job)
        db.commit()
        return {"message": "Job deleted successfully"}