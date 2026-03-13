"""
StudentTrack — Seed Script
Run: python seed.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.company import Company
from app.models.coordinator import Coordinator
from app.models.job_posting import JobPosting, JobType, JobStatus
from app.models.application import Application, ApplicationStatus
from app.models.application_log import ApplicationStatusLog
from app.core.security import hash_password
from datetime import datetime, timedelta


def seed():
    db = SessionLocal()

    print("🌱 Starting seed...")

    # ── Check already seeded ───────────────────────────
    if db.query(User).count() > 0:
        print("⚠️  Database already has data. Skipping seed.")
        print("   To reseed, clear all tables first.")
        db.close()
        return

    # ══════════════════════════════════════════════════
    # 1. COORDINATOR (Admin)
    # ══════════════════════════════════════════════════
    coord_user = User(
        email="admin@studenttrack.com",
        password_hash=hash_password("admin123"),
        role=UserRole.COORDINATOR,
        is_active=True
    )
    db.add(coord_user)
    db.commit()
    db.refresh(coord_user)

    coordinator = Coordinator(
        user_id=coord_user.id,
        full_name="Dr. Nguyen Van An",
        department="Career Development Center",
        phone="0901234567"
    )
    db.add(coordinator)
    db.commit()
    print("✅ Coordinator created")

    # ══════════════════════════════════════════════════
    # 2. COMPANIES
    # ══════════════════════════════════════════════════
    companies_data = [
        {
            "email": "hr@techviet.com",
            "name": "TechViet Solutions",
            "description": "Leading software development company in Vietnam specializing in fintech and e-commerce solutions.",
            "website": "https://techviet.com",
            "location": "Ho Chi Minh City",
            "contact_email": "hr@techviet.com",
            "contact_phone": "0281234567",
        },
        {
            "email": "recruit@fpt.com",
            "name": "FPT Software",
            "description": "Vietnam's largest IT company with global presence in 29 countries.",
            "website": "https://fptsoftware.com",
            "location": "Ha Noi",
            "contact_email": "recruit@fpt.com",
            "contact_phone": "0247654321",
        },
        {
            "email": "jobs@vingroup.net",
            "name": "VinGroup Technology",
            "description": "Technology division of Vietnam's largest private conglomerate.",
            "website": "https://vingroup.net",
            "location": "Ho Chi Minh City",
            "contact_email": "jobs@vingroup.net",
            "contact_phone": "0289876543",
        },
    ]

    company_objects = []
    for c in companies_data:
        user = User(
            email=c["email"],
            password_hash=hash_password("company123"),
            role=UserRole.COMPANY,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        company = Company(
            user_id=user.id,
            name=c["name"],
            description=c["description"],
            website=c["website"],
            location=c["location"],
            contact_email=c["contact_email"],
            contact_phone=c["contact_phone"],
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        company_objects.append(company)

    print(f"✅ {len(company_objects)} companies created")

    # ══════════════════════════════════════════════════
    # 3. STUDENTS
    # ══════════════════════════════════════════════════
    students_data = [
        {
            "email": "minh.nguyen@student.edu.vn",
            "full_name": "Nguyen Thanh Minh",
            "student_id": "SE210001",
            "major": "Software Engineering",
            "gpa": 3.8,
            "phone": "0901111111",
            "graduation_year": 2025,
            "bio": "Passionate backend developer with strong Python and FastAPI skills. Looking for internship opportunities.",
            "resume_url": "https://drive.google.com/resume-minh"
        },
        {
            "email": "linh.tran@student.edu.vn",
            "full_name": "Tran Thi Linh",
            "student_id": "SE210002",
            "major": "Computer Science",
            "gpa": 3.5,
            "phone": "0902222222",
            "graduation_year": 2025,
            "bio": "Frontend developer interested in UI/UX design and React development.",
            "resume_url": "https://drive.google.com/resume-linh"
        },
        {
            "email": "huy.le@student.edu.vn",
            "full_name": "Le Van Huy",
            "student_id": "SE210003",
            "major": "Information Technology",
            "gpa": 3.2,
            "phone": "0903333333",
            "graduation_year": 2026,
            "bio": "Full-stack developer with experience in Node.js and Vue.js.",
            "resume_url": "https://drive.google.com/resume-huy"
        },
        {
            "email": "an.pham@student.edu.vn",
            "full_name": "Pham Thi An",
            "student_id": "SE210004",
            "major": "Software Engineering",
            "gpa": 3.9,
            "phone": "0904444444",
            "graduation_year": 2025,
            "bio": "AI/ML enthusiast with Python and TensorFlow experience. Dean's list student.",
            "resume_url": "https://drive.google.com/resume-an"
        },
        {
            "email": "khoa.vo@student.edu.vn",
            "full_name": "Vo Minh Khoa",
            "student_id": "SE210005",
            "major": "Computer Science",
            "gpa": 3.0,
            "phone": "0905555555",
            "graduation_year": 2026,
            "bio": "Backend developer learning cloud infrastructure and DevOps practices.",
            "resume_url": "https://drive.google.com/resume-khoa"
        },
    ]

    student_objects = []
    for s in students_data:
        user = User(
            email=s["email"],
            password_hash=hash_password("student123"),
            role=UserRole.STUDENT,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        student = Student(
            user_id=user.id,
            full_name=s["full_name"],
            student_id=s["student_id"],
            major=s["major"],
            gpa=s["gpa"],
            phone=s["phone"],
            graduation_year=s["graduation_year"],
            bio=s["bio"],
            resume_url=s["resume_url"]
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        student_objects.append(student)

    print(f"✅ {len(student_objects)} students created")

    # ══════════════════════════════════════════════════
    # 4. JOB POSTINGS
    # ══════════════════════════════════════════════════
    jobs_data = [
        {
            "company": company_objects[0],  # TechViet
            "title": "Python Backend Developer Intern",
            "description": "Join our backend team to build scalable REST APIs using Python and FastAPI. Work on real fintech products used by thousands of users.",
            "requirements": "4th-year student in CS/SE/IT. Strong Python skills. Knowledge of SQL and Git. FastAPI or Django experience is a plus.",
            "location": "Ho Chi Minh City",
            "job_type": JobType.INTERNSHIP,
            "salary_min": 5000000,
            "salary_max": 8000000,
            "status": JobStatus.OPEN,
            "deadline": datetime.utcnow() + timedelta(days=30),
        },
        {
            "company": company_objects[0],  # TechViet
            "title": "Junior Full-Stack Developer",
            "description": "We are looking for a full-stack developer to join our product team. You will work on both frontend and backend features.",
            "requirements": "Fresh graduate or 1 year experience. React, Node.js or Python. Good understanding of databases.",
            "location": "Ho Chi Minh City",
            "job_type": JobType.FULL_TIME,
            "salary_min": 12000000,
            "salary_max": 18000000,
            "status": JobStatus.OPEN,
            "deadline": datetime.utcnow() + timedelta(days=45),
        },
        {
            "company": company_objects[1],  # FPT
            "title": "Software Engineer Intern",
            "description": "FPT Software internship program — 4 months working on enterprise software projects with mentorship from senior engineers.",
            "requirements": "3rd or 4th year CS/SE student. Java or Python. Good English communication skills.",
            "location": "Ha Noi",
            "job_type": JobType.INTERNSHIP,
            "salary_min": 4000000,
            "salary_max": 6000000,
            "status": JobStatus.OPEN,
            "deadline": datetime.utcnow() + timedelta(days=20),
        },
        {
            "company": company_objects[1],  # FPT
            "title": "Data Analyst — Part Time",
            "description": "Analyze business data and create reports to support decision making. Flexible working hours suitable for students.",
            "requirements": "SQL proficiency required. Python or R for data analysis. Tableau or Power BI is a plus.",
            "location": "Ha Noi",
            "job_type": JobType.PART_TIME,
            "salary_min": 6000000,
            "salary_max": 9000000,
            "status": JobStatus.OPEN,
            "deadline": datetime.utcnow() + timedelta(days=25),
        },
        {
            "company": company_objects[2],  # VinGroup
            "title": "AI/ML Engineer Intern",
            "description": "Work with our AI team on computer vision and NLP projects. Access to cutting-edge infrastructure and datasets.",
            "requirements": "Strong Python. Experience with TensorFlow or PyTorch. Mathematics background (linear algebra, statistics).",
            "location": "Ho Chi Minh City",
            "job_type": JobType.INTERNSHIP,
            "salary_min": 7000000,
            "salary_max": 10000000,
            "status": JobStatus.OPEN,
            "deadline": datetime.utcnow() + timedelta(days=15),
        },
        {
            "company": company_objects[2],  # VinGroup
            "title": "DevOps Engineer",
            "description": "Manage CI/CD pipelines, cloud infrastructure on AWS, and container orchestration with Kubernetes.",
            "requirements": "1+ year experience. Docker, Kubernetes, AWS or GCP. Strong Linux skills.",
            "location": "Ho Chi Minh City",
            "job_type": JobType.FULL_TIME,
            "salary_min": 20000000,
            "salary_max": 30000000,
            "status": JobStatus.DRAFT,
            "deadline": datetime.utcnow() + timedelta(days=60),
        },
    ]

    job_objects = []
    for j in jobs_data:
        job = JobPosting(
            company_id=j["company"].id,
            title=j["title"],
            description=j["description"],
            requirements=j["requirements"],
            location=j["location"],
            job_type=j["job_type"],
            salary_min=j["salary_min"],
            salary_max=j["salary_max"],
            status=j["status"],
            deadline=j["deadline"],
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        job_objects.append(job)

    print(f"✅ {len(job_objects)} job postings created")

    # ══════════════════════════════════════════════════
    # 5. APPLICATIONS
    # ══════════════════════════════════════════════════
    applications_data = [
        # Minh applies to Python Backend Intern → accepted
        {
            "student": student_objects[0],
            "job": job_objects[0],
            "cover_letter": "I am a 4th-year SE student with strong Python and FastAPI skills. I have built a full-stack project using FastAPI and PostgreSQL. I am very excited about this opportunity at TechViet.",
            "status": ApplicationStatus.ACCEPTED,
        },
        # Minh applies to FPT intern → reviewing
        {
            "student": student_objects[0],
            "job": job_objects[2],
            "cover_letter": "I would love to gain experience at FPT Software. My GPA is 3.8 and I have solid Java knowledge alongside Python.",
            "status": ApplicationStatus.REVIEWING,
        },
        # Linh applies to Junior Full-Stack → interview
        {
            "student": student_objects[1],
            "job": job_objects[1],
            "cover_letter": "As a CS graduate with frontend experience in React and backend in Node.js, I am confident I can contribute to your product team.",
            "status": ApplicationStatus.INTERVIEW,
        },
        # Linh applies to Data Analyst → pending
        {
            "student": student_objects[1],
            "job": job_objects[3],
            "cover_letter": "I have experience with SQL and Python pandas for data analysis. I am available for part-time work on weekends.",
            "status": ApplicationStatus.PENDING,
        },
        # Huy applies to FPT intern → rejected
        {
            "student": student_objects[2],
            "job": job_objects[2],
            "cover_letter": "I am a 3rd-year IT student eager to learn enterprise software development at FPT.",
            "status": ApplicationStatus.REJECTED,
        },
        # An applies to AI/ML intern → interview
        {
            "student": student_objects[3],
            "job": job_objects[4],
            "cover_letter": "I have hands-on experience with TensorFlow and PyTorch from university projects. My GPA is 3.9 and I ranked top of my class in Machine Learning course.",
            "status": ApplicationStatus.INTERVIEW,
        },
        # Khoa applies to Python Backend → pending
        {
            "student": student_objects[4],
            "job": job_objects[0],
            "cover_letter": "I am learning Python backend development and would love to apply my skills in a real-world environment.",
            "status": ApplicationStatus.PENDING,
        },
        # An applies to Full-Stack → reviewing
        {
            "student": student_objects[3],
            "job": job_objects[1],
            "cover_letter": "Although my main strength is AI/ML, I also have solid Python backend experience and would love to grow as a full-stack developer.",
            "status": ApplicationStatus.REVIEWING,
        },
    ]

    application_objects = []
    for a in applications_data:
        application = Application(
            student_id=a["student"].id,
            job_id=a["job"].id,
            cover_letter=a["cover_letter"],
            status=a["status"],
            applied_at=datetime.utcnow() - timedelta(days=len(application_objects) + 1)
        )
        db.add(application)
        db.commit()
        db.refresh(application)
        application_objects.append(application)

        # create status log
        log = ApplicationStatusLog(
            application_id=application.id,
            old_status=ApplicationStatus.PENDING,
            new_status=a["status"],
            changed_by=coord_user.id,
            note="Initial status set by system"
        )
        db.add(log)
        db.commit()

    print(f"✅ {len(application_objects)} applications created")

    # ══════════════════════════════════════════════════
    # SUMMARY
    # ══════════════════════════════════════════════════
    print("\n" + "="*50)
    print("🎉 Seed completed successfully!")
    print("="*50)
    print("\n📋 Login accounts:")
    print("\n[Coordinator]")
    print("  Email:    admin@studenttrack.com")
    print("  Password: admin123")
    print("\n[Companies]")
    for c in companies_data:
        print(f"  Email:    {c['email']}")
        print(f"  Password: company123")
        print(f"  Name:     {c['name']}")
    print("\n[Students]")
    for s in students_data:
        print(f"  Email:    {s['email']}")
        print(f"  Password: student123")
        print(f"  Name:     {s['full_name']}")
    print("="*50)

    db.close()


if __name__ == "__main__":
    seed()