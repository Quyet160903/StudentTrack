from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.models.company import Company
from app.models.job_posting import JobPosting, JobStatus
from app.schemas.job import JobCreate, JobUpdate, JobApprovalAction, JobResponse


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
            status=JobStatus.PENDING,   # always force PENDING on create
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return JobResponse.model_validate(job)

    @staticmethod
    def get_all(db: Session) -> List[JobResponse]:
        """Public — students and companies browsing: only OPEN jobs."""
        jobs = db.query(JobPosting).filter(JobPosting.status == JobStatus.OPEN).all()
        return [JobResponse.model_validate(j) for j in jobs]

    @staticmethod
    def get_all_for_coordinator(db: Session) -> List[JobResponse]:
        """Coordinator — sees every job regardless of status."""
        jobs = db.query(JobPosting).all()
        return [JobResponse.model_validate(j) for j in jobs]

    @staticmethod
    def get_pending(db: Session) -> List[JobResponse]:
        """Coordinator — pending approval queue."""
        jobs = db.query(JobPosting).filter(JobPosting.status == JobStatus.PENDING).all()
        return [JobResponse.model_validate(j) for j in jobs]

    @staticmethod
    def get_by_company(db: Session, current_user: User) -> List[JobResponse]:
        """Company — their own jobs (all statuses)."""
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company profile not found")
        jobs = db.query(JobPosting).filter(JobPosting.company_id == company.id).all()
        return [JobResponse.model_validate(j) for j in jobs]

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

        if request.status in (JobStatus.OPEN, JobStatus.CLOSED, JobStatus.DRAFT):
            if job.status != JobStatus.APPROVED:
                raise HTTPException(
                    status_code=400,
                    detail="Job must be approved by coordinator before publishing"
                )

        for field, value in request.model_dump(exclude_none=True).items():
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