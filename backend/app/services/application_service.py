from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate, ApplicationStatus

from app.models.user import User
from app.models.job_posting import JobPosting, JobStatus
from app.models.application import Application
from app.models.application_log import ApplicationStatusLog

class ApplicationService:
    @staticmethod
    def apply(db: Session, request: ApplicationCreate, current_user: User) -> ApplicationResponse:
        job_posting = db.query(JobPosting).filter(JobPosting.id == request.job_id).first()
        if not job_posting:
            raise HTTPException(
                status_code=404,
                detail="Job posting not found"
            )
        
        if job_posting.status != JobStatus.OPEN:
            raise HTTPException(
                status_code=400,
                detail="Job posting not open"
            )
        
        existing = db.query(Application).filter(
            Application.student_id == current_user.student.id,
            Application.job_id == request.job_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="You have already applied this job"
            )
        
        application = Application(
            student_id=current_user.student.id,
            job_id=job_posting.id,
            cover_letter=request.cover_letter,
            resume_url=request.resume_url,
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return ApplicationResponse.model_validate(application)
    
    @staticmethod
    def get_all(db: Session) -> List[ApplicationResponse]:
        applications = db.query(Application).all()
        return [ApplicationResponse.model_validate(app) for app in applications]
    
    @staticmethod
    def get_my_applications(db: Session, current_user: User) -> List[ApplicationResponse]:
        applications = current_user.student.applications

        return [ApplicationResponse.model_validate(application) for application in applications]
    
    @staticmethod
    def get_job_applications(db: Session, job_id: int, current_user: User) -> List[ApplicationResponse]:
        job_posting = db.query(JobPosting).filter(JobPosting.id==job_id).first()
        if not job_posting:
            raise HTTPException(
                status_code=404,
                detail="Job posting not found"
            )
        
        if job_posting.company_id != current_user.company.id:
            raise HTTPException(status_code=403, detail="You can only view your own job applications")
        
        applications = job_posting.applications

        return [ApplicationResponse.model_validate(application) for application in applications]
    
    @staticmethod
    def update_status(db: Session, app_id: int, request: ApplicationUpdate, current_user: User) -> ApplicationResponse:
        application = db.query(Application).filter(Application.id==app_id).first()
        if not application:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )
        
        if current_user.is_coordinator:
            pass
        elif current_user.is_company:
            if application.job.company_id != current_user.company.id:
                raise HTTPException(
                    status_code=403,
                    detail="You can only update your own job applications"
                )
        elif current_user.is_student:
            if application.student_id != current_user.student.id:
                raise HTTPException(status_code=403, detail="You can only withdraw your own applications")
            if request.status != ApplicationStatus.WITHDRAWN:
                raise HTTPException(status_code=403, detail="Students can only withdraw applications")
        else:
            raise HTTPException(status_code=403,
                                detail="Not authorized")
        
        log = ApplicationStatusLog(
            application_id=application.id,
            old_status=application.status,
            new_status=request.status,
            changed_by=current_user.id,
            note=request.note
        )
        db.add(log)
            
        application.status = request.status
        
        db.commit()
        db.refresh(application)

        return ApplicationResponse.model_validate(application)