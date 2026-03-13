from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.models.student import Student
from app.models.company import Company
from app.models.job_posting import JobPosting, JobStatus
from app.models.application import Application, ApplicationStatus
from app.models.application_log import ApplicationStatusLog
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from app.schemas.application_log import ApplicationLogResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse


class ApplicationService:

    @staticmethod
    def create(db: Session, request: ApplicationCreate, current_user: User) -> ApplicationResponse:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        job = db.query(JobPosting).filter(JobPosting.id == request.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.status != JobStatus.OPEN:
            raise HTTPException(status_code=400, detail="Job is not open for applications")

        # prevent duplicate application
        existing = db.query(Application).filter(
            Application.student_id == student.id,
            Application.job_id == request.job_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="You have already applied to this job")

        app = Application(
            student_id=student.id,
            job_id=request.job_id,
            cover_letter=request.cover_letter,
            resume_url=request.resume_url,
            status=ApplicationStatus.PENDING,
        )
        db.add(app)
        db.commit()
        db.refresh(app)
        return ApplicationResponse.model_validate(app)

    @staticmethod
    def get_my_applications(db: Session, current_user: User) -> List[ApplicationResponse]:
        """Student — their own applications."""
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")
        apps = db.query(Application).filter(Application.student_id == student.id).all()
        return [ApplicationResponse.model_validate(a) for a in apps]

    @staticmethod
    def get_by_job(db: Session, job_id: int, current_user: User) -> List[ApplicationResponse]:
        """Company — all applicants for one of their jobs."""
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company profile not found")
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.company_id != company.id:
            raise HTTPException(status_code=403, detail="Not your job")
        apps = db.query(Application).filter(Application.job_id == job_id).all()
        return [ApplicationResponse.model_validate(a) for a in apps]

    @staticmethod
    def get_all(
        db: Session,
        params: PaginationParams,
        status: ApplicationStatus | None = None,
    ) -> PaginatedResponse[ApplicationResponse]:
        """
        Coordinator — all applications across the platform, paginated.

        GET /applications/all?page=1&page_size=15
        GET /applications/all?page=1&page_size=15&status=accepted
        Returns: { items, total, page, page_size, total_pages }
        """
        query = db.query(Application)
        if status:
            query = query.filter(Application.status == status)
        total = query.count()
        apps = (
            query
            .order_by(Application.applied_at.desc())   # newest first
            .offset(params.offset)
            .limit(params.page_size)
            .all()
        )
        return PaginatedResponse.create(
            items=[ApplicationResponse.model_validate(a) for a in apps],
            total=total,
            params=params,
        )

    @staticmethod
    def update_status(
        db: Session,
        app_id: int,
        request: ApplicationUpdate,
        current_user: User
    ) -> ApplicationResponse:
        """
        Update application status.
        - Company: can set reviewing / interview / accepted / rejected (own jobs only)
        - Coordinator: can set any status
        - Student: can only withdraw their own application
        """
        app = db.query(Application).filter(Application.id == app_id).first()
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        from app.models.user import UserRole

        if current_user.role == UserRole.STUDENT:
            # student can only withdraw their own application
            student = db.query(Student).filter(Student.user_id == current_user.id).first()
            if not student or app.student_id != student.id:
                raise HTTPException(status_code=403, detail="Not your application")
            if request.status != ApplicationStatus.WITHDRAWN:
                raise HTTPException(status_code=403, detail="Students can only withdraw applications")

        elif current_user.role == UserRole.COMPANY:
            # company can only update applications for their own jobs
            company = db.query(Company).filter(Company.user_id == current_user.id).first()
            if not company:
                raise HTTPException(status_code=404, detail="Company profile not found")
            job = db.query(JobPosting).filter(JobPosting.id == app.job_id).first()
            if job.company_id != company.id:
                raise HTTPException(status_code=403, detail="Not your job")

        old_status = app.status
        app.status = request.status
        db.commit()
        db.refresh(app)

        # Write status change log
        log = ApplicationStatusLog(
            application_id=app.id,
            old_status=old_status,
            new_status=request.status,
            changed_by=current_user.id,
            note=request.note if hasattr(request, 'note') else None,
        )
        db.add(log)
        db.commit()

        return ApplicationResponse.model_validate(app)

    @staticmethod
    def get_logs(db: Session, app_id: int, current_user: User) -> List[ApplicationLogResponse]:
        """
        Return status change history for one application.
        Accessible by: coordinator, the company that owns the job, the student who applied.
        """
        from app.models.user import UserRole

        app = db.query(Application).filter(Application.id == app_id).first()
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        # Authorization check
        if current_user.role == UserRole.STUDENT:
            student = db.query(Student).filter(Student.user_id == current_user.id).first()
            if not student or app.student_id != student.id:
                raise HTTPException(status_code=403, detail="Not your application")
        elif current_user.role == UserRole.COMPANY:
            company = db.query(Company).filter(Company.user_id == current_user.id).first()
            job = db.query(JobPosting).filter(JobPosting.id == app.job_id).first()
            if not company or job.company_id != company.id:
                raise HTTPException(status_code=403, detail="Not your job")
        # coordinator can see all

        logs = (
            db.query(ApplicationStatusLog)
            .filter(ApplicationStatusLog.application_id == app_id)
            .order_by(ApplicationStatusLog.changed_at.asc())
            .all()
        )
        return [ApplicationLogResponse.model_validate(log) for log in logs]