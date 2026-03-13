from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.company import CompanyResponse, CompanyUpdate
from app.services.company_service import CompanyService
from app.core.deps import require_company, require_coordinator

company_router = APIRouter(prefix="/companies", tags=["companies"])

@company_router.get("/", response_model=List[CompanyResponse])
def get_all_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_coordinator)
):
    return CompanyService.get_all(db)

@company_router.get("/profile", response_model=CompanyResponse)
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(require_company)):
    return CompanyService.get_profile(db, current_user)

@company_router.put("/profile", response_model=CompanyResponse)
def update_profile(request: CompanyUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_company)):
    return CompanyService.update_profile(db, request, current_user)