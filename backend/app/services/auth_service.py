from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, TokenResponse, UserResponse
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.company import Company
from app.models.coordinator import Coordinator
from app.models.application import Application
from app.models.application_log import ApplicationStatusLog
from app.models.job_posting import JobPosting

from app.models.refresh_token import RefreshToken as RefreshTokenModel

class AuthService:

    @staticmethod
    def register(db: Session, request: RegisterRequest) -> UserResponse:
        # block coordinator self-registration
        if request.role == UserRole.COORDINATOR:
            raise HTTPException(
                status_code=403,
                detail="Coordinator accounts cannot be self-registered"
            )
        
        # 1. check duplicate email
        existing = db.query(User).filter(User.email == request.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")   

        # 2. create user
        user = User(
            email=request.email,
            password_hash=hash_password(request.password),
            role=request.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # 3. create profile based on role
        if request.role == UserRole.STUDENT:
            profile = Student(user_id=user.id)
            db.add(profile)
        elif request.role == UserRole.COMPANY:
            profile = Company(user_id=user.id)
            db.add(profile)

        db.commit()
        return UserResponse.model_validate(user)

    @staticmethod
    def login(db: Session, request: LoginRequest) -> TokenResponse:
        # 1. find user
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 2. verify password
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect password")

        # 3. create tokens
        access_token = create_access_token(data={
            "sub": str(user.id),
            "role": user.role
        })
        refresh_token = create_refresh_token(data={
            "sub": str(user.id)
        })

        # 4. save refresh token to db
        token = RefreshTokenModel(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(token)
        db.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    def refresh(db: Session, request: RefreshRequest) -> TokenResponse:
        # 1. find token in db
        token = db.query(RefreshTokenModel).filter(
            RefreshTokenModel.token == request.refresh_token
        ).first()
        if not token:
            raise HTTPException(status_code=404, detail="Refresh token not found")

        # 2. check revoked
        if token.revoked:
            raise HTTPException(status_code=401, detail="Refresh token has been revoked")

        # 3. check expired
        if token.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # 4. decode token to get user info
        payload = decode_token(token.token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        # 5. revoke old token
        token.revoked = True
        db.commit()

        # 6. create new tokens
        new_access_token = create_access_token(data={
            "sub": payload.get("sub"),
            "role": payload.get("role")
        })
        new_refresh_token = create_refresh_token(data={
            "sub": payload.get("sub")
        })

        # 7. save new refresh token
        new_token = RefreshTokenModel(
            user_id=int(payload.get("sub")),
            token=new_refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(new_token)
        db.commit()

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )