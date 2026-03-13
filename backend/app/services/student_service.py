from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.models.student import Student
from app.schemas.student import StudentUpdate, StudentResponse


class StudentService:

    @staticmethod
    def get_all(db: Session) -> List[StudentResponse]:
        students = db.query(Student).all()
        return [StudentResponse.model_validate(s) for s in students]

    @staticmethod
    def get_profile(db: Session, current_user: User) -> StudentResponse:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")
        return StudentResponse.model_validate(student)

    @staticmethod
    def update_profile(db: Session, request: StudentUpdate, current_user: User) -> StudentResponse:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        if request.full_name is not None:
            student.full_name = request.full_name
        if request.student_id is not None:
            student.student_id = request.student_id
        if request.major is not None:
            student.major = request.major
        if request.gpa is not None:
            student.gpa = request.gpa
        if request.phone is not None:
            student.phone = request.phone
        if request.graduation_year is not None:
            student.graduation_year = request.graduation_year
        if request.resume_url is not None:
            student.resume_url = request.resume_url
        if request.bio is not None:
            student.bio = request.bio

        db.commit()
        db.refresh(student)
        return StudentResponse.model_validate(student)