from pydantic import BaseModel, EmailStr, field_validator
from app.models.user import UserRole

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(LoginRequest):
    role: UserRole

    @field_validator("role")
    @classmethod
    def role_must_be_allowed(cls, v):
        allowed = [UserRole.STUDENT, UserRole.COMPANY]
        if v not in allowed:
            raise ValueError("Role must be student or company")
        return v

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole

    class Config:
        from_attributes = True