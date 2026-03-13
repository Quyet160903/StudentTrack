from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.company import Company
from app.schemas.company import CompanyUpdate, CompanyResponse


class CompanyService:

    @staticmethod
    def get_profile(db: Session, current_user: User) -> CompanyResponse:
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company profile not found")
        return CompanyResponse.model_validate(company)
    
    @staticmethod
    def get_all(db: Session):
        companies = db.query(Company).all()
        return [CompanyResponse.model_validate(c) for c in companies]

    @staticmethod
    def update_profile(db: Session, request: CompanyUpdate, current_user: User) -> CompanyResponse:
        company = db.query(Company).filter(Company.user_id == current_user.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company profile not found")

        if request.name is not None:
            company.name = request.name
        if request.description is not None:
            company.description = request.description
        if request.website is not None:
            company.website = request.website
        if request.location is not None:
            company.location = request.location
        if request.contact_email is not None:
            company.contact_email = request.contact_email
        if request.contact_phone is not None:
            company.contact_phone = request.contact_phone
        if request.logo_url is not None:
            company.logo_url = request.logo_url

        db.commit()
        db.refresh(company)
        return CompanyResponse.model_validate(company)