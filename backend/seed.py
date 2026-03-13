"""
StudentTrack — Seed Script
Run from backend/ folder: python seed.py

Data:
  1  coordinator
  5  companies (TechViet, FPT, VinGroup, MoMo, Tiki)
  8  students
  30 job postings (25 OPEN, 3 PENDING, 1 APPROVED, 1 REJECTED)
  20 applications
"""
import sys, os
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

    if db.query(User).count() > 0:
        print("⚠️  Database already has data. Skipping seed.")
        print("   To reseed: truncate all tables and run again.")
        db.close()
        return

    # ── 1. COORDINATOR ────────────────────────────────────
    coord_user = User(email="admin@studenttrack.com",
                      password_hash=hash_password("admin123"),
                      role=UserRole.COORDINATOR, is_active=True)
    db.add(coord_user); db.commit(); db.refresh(coord_user)
    db.add(Coordinator(user_id=coord_user.id, full_name="Dr. Nguyen Van An",
                       department="Career Development Center", phone="0901234567"))
    db.commit()
    print("✅ Coordinator created")

    # ── 2. COMPANIES ──────────────────────────────────────
    companies_raw = [
        ("hr@techviet.com",    "TechViet Solutions",   "Ho Chi Minh City", "https://techviet.com",     "Leading fintech & e-commerce software house."),
        ("recruit@fpt.com",    "FPT Software",         "Ha Noi",           "https://fptsoftware.com",   "Vietnam's largest IT company, 29 countries."),
        ("jobs@vingroup.net",  "VinGroup Technology",  "Ho Chi Minh City", "https://vingroup.net",      "Tech division of Vietnam's largest conglomerate."),
        ("talent@momo.vn",     "MoMo E-Wallet",        "Ho Chi Minh City", "https://momo.vn",           "Vietnam's leading fintech platform, 31M users."),
        ("careers@tiki.vn",    "Tiki Corporation",     "Ho Chi Minh City", "https://tiki.vn",           "Top e-commerce platform, technology-first."),
    ]
    company_objects = []
    for email, name, loc, web, desc in companies_raw:
        u = User(email=email, password_hash=hash_password("company123"),
                 role=UserRole.COMPANY, is_active=True)
        db.add(u); db.commit(); db.refresh(u)
        c = Company(user_id=u.id, name=name, description=desc,
                    website=web, location=loc, contact_email=email)
        db.add(c); db.commit(); db.refresh(c)
        company_objects.append(c)
    print(f"✅ {len(company_objects)} companies created")
    tv, fpt, vin, mo, tk = company_objects

    # ── 3. STUDENTS ───────────────────────────────────────
    students_raw = [
        ("minh.nguyen@student.edu.vn", "Nguyen Thanh Minh", "SE210001", "Software Engineering",  3.8, 2025, "Backend dev, Python & FastAPI."),
        ("linh.tran@student.edu.vn",   "Tran Thi Linh",     "SE210002", "Computer Science",       3.5, 2025, "Frontend dev, React & UI/UX."),
        ("huy.le@student.edu.vn",      "Le Van Huy",         "SE210003", "Information Technology", 3.2, 2026, "Full-stack, Node.js & Vue.js."),
        ("an.pham@student.edu.vn",     "Pham Thi An",        "SE210004", "Software Engineering",   3.9, 2025, "AI/ML, TensorFlow & PyTorch."),
        ("khoa.vo@student.edu.vn",     "Vo Minh Khoa",       "SE210005", "Computer Science",       3.0, 2026, "Backend, learning DevOps."),
        ("tuan.nguyen@student.edu.vn", "Nguyen Duc Tuan",    "SE210006", "Software Engineering",   3.6, 2025, "Mobile dev, Flutter & RN."),
        ("mai.le@student.edu.vn",      "Le Thi Mai",         "SE210007", "Data Science",           3.7, 2025, "Data scientist, Python & SQL."),
        ("long.pham@student.edu.vn",   "Pham Hoang Long",    "SE210008", "Computer Science",       3.4, 2026, "Security, CTF enthusiast."),
    ]
    student_objects = []
    for email, name, sid, major, gpa, grad, bio in students_raw:
        u = User(email=email, password_hash=hash_password("student123"),
                 role=UserRole.STUDENT, is_active=True)
        db.add(u); db.commit(); db.refresh(u)
        s = Student(user_id=u.id, full_name=name, student_id=sid, major=major,
                    gpa=gpa, graduation_year=grad, bio=bio,
                    phone=f"090{sid[-4:]}",
                    resume_url=f"https://drive.google.com/resume-{email.split('.')[0]}")
        db.add(s); db.commit(); db.refresh(s)
        student_objects.append(s)
    print(f"✅ {len(student_objects)} students created")

    # ── 4. JOBS (30 total) ────────────────────────────────
    D = lambda n: datetime.utcnow() + timedelta(days=n)
    O, I, F, P = JobStatus.OPEN, JobType.INTERNSHIP, JobType.FULL_TIME, JobType.PART_TIME

    jobs_data = [
        # TechViet (6)
        (tv,  "Python Backend Developer Intern",        I, "Ho Chi Minh City",  5e6,  8e6, O, D(30), None),
        (tv,  "Junior Full-Stack Developer",            F, "Ho Chi Minh City", 12e6, 18e6, O, D(45), None),
        (tv,  "React Frontend Developer",               F, "Ho Chi Minh City", 15e6, 22e6, O, D(40), None),
        (tv,  "QA Engineer — Part Time",                P, "Ho Chi Minh City",  6e6,  9e6, O, D(20), None),
        (tv,  "Database Administrator Intern",          I, "Ho Chi Minh City",  4e6,  6e6, O, D(25), None),
        (tv,  "Cloud Infrastructure Engineer",          F, "Ho Chi Minh City", 25e6, 35e6, O, D(60), None),
        # FPT (6)
        (fpt, "Software Engineer Intern",               I, "Ha Noi",             4e6,  6e6, O, D(20), None),
        (fpt, "Data Analyst — Part Time",               P, "Ha Noi",             6e6,  9e6, O, D(25), None),
        (fpt, "Java Backend Engineer",                  F, "Ha Noi",            18e6, 28e6, O, D(35), None),
        (fpt, "Business Analyst Intern",                I, "Ha Noi",             3e6,  5e6, O, D(18), None),
        (fpt, "Mobile Developer — React Native",        F, "Ha Noi",            20e6, 30e6, O, D(50), None),
        (fpt, "Technical Writer — Part Time",           P, "Ha Noi",             5e6,  7e6, O, D(15), None),
        # VinGroup (5)
        (vin, "AI/ML Engineer Intern",                  I, "Ho Chi Minh City",   7e6, 10e6, O, D(15), None),
        (vin, "DevOps Engineer",                        F, "Ho Chi Minh City",  20e6, 30e6, O, D(60), None),
        (vin, "Data Engineer",                          F, "Ha Noi",            22e6, 32e6, O, D(40), None),
        (vin, "Cybersecurity Analyst Intern",           I, "Ho Chi Minh City",   5e6,  8e6, O, D(22), None),
        (vin, "Product Manager — Associate",            F, "Ho Chi Minh City",  18e6, 28e6, O, D(55), None),
        # MoMo (6)
        (mo,  "iOS Developer Intern",                   I, "Ho Chi Minh City",   6e6,  9e6, O, D(28), None),
        (mo,  "Android Developer",                      F, "Ho Chi Minh City",  20e6, 32e6, O, D(45), None),
        (mo,  "Machine Learning Engineer",              F, "Ho Chi Minh City",  28e6, 45e6, O, D(50), None),
        (mo,  "UI/UX Designer Intern",                  I, "Ho Chi Minh City",   4e6,  6e6, O, D(20), None),
        (mo,  "Backend Engineer — Payment Systems",     F, "Ho Chi Minh City",  35e6, 55e6, O, D(60), None),
        (mo,  "Data Scientist — Part Time",             P, "Ho Chi Minh City",   8e6, 12e6, O, D(30), None),
        # Tiki (4 OPEN)
        (tk,  "E-commerce Platform Engineer",           F, "Ho Chi Minh City",  25e6, 40e6, O, D(45), None),
        (tk,  "Logistics Tech Intern",                  I, "Ho Chi Minh City",   5e6,  7e6, O, D(25), None),
        (tk,  "Search & Recommendation Engineer",       F, "Ho Chi Minh City",  30e6, 45e6, O, D(55), None),
        (tk,  "Frontend Engineer — Next.js",            F, "Ho Chi Minh City",  20e6, 32e6, O, D(40), None),
        # Non-OPEN (3 PENDING, 1 APPROVED, 1 REJECTED)
        (tk,  "Blockchain Engineer",                    F, "Ho Chi Minh City",  30e6, 50e6, JobStatus.PENDING,  D(60), None),
        (mo,  "Site Reliability Engineer",              F, "Ho Chi Minh City",  35e6, 50e6, JobStatus.PENDING,  D(45), None),
        (fpt, "Salesforce Developer",                   F, "Ha Noi",            20e6, 30e6, JobStatus.PENDING,  D(30), None),
        (vin, "Middle AI Engineer",                     F, "Ho Chi Minh City",  20e6, 35e6, JobStatus.APPROVED, None,  None),
        (tv,  "AR/VR Developer",                        F, "Ho Chi Minh City",  22e6, 33e6, JobStatus.REJECTED, D(30), "Description too vague. Please specify Unity version and project scope."),
    ]

    job_objects = []
    for co, title, jtype, loc, smin, smax, status, deadline, note in jobs_data:
        job = JobPosting(company_id=co.id, title=title, job_type=jtype, location=loc,
                         salary_min=smin, salary_max=smax, status=status,
                         deadline=deadline, rejection_note=note,
                         description=f"Position: {title} at {co.name}.",
                         requirements="Relevant degree or equivalent experience required.")
        db.add(job); db.commit(); db.refresh(job)
        job_objects.append(job)

    open_jobs = [j for j in job_objects if j.status == JobStatus.OPEN]
    print(f"✅ {len(job_objects)} jobs created ({len(open_jobs)} OPEN, "
          f"{sum(1 for j in job_objects if j.status==JobStatus.PENDING)} PENDING, "
          f"{sum(1 for j in job_objects if j.status==JobStatus.APPROVED)} APPROVED, "
          f"{sum(1 for j in job_objects if j.status==JobStatus.REJECTED)} REJECTED)")

    # ── 5. APPLICATIONS (20) ──────────────────────────────
    mn, lt, lh, pa, vk, nt, lm, pl = student_objects
    apps_data = [
        (mn, open_jobs[0],  "4th-year SE, strong FastAPI. Built full-stack app.",              ApplicationStatus.ACCEPTED),
        (mn, open_jobs[6],  "GPA 3.8, Java + Python. Eager for FPT projects.",                ApplicationStatus.REVIEWING),
        (mn, open_jobs[1],  "Strong Python. Ready to expand to full-stack.",                   ApplicationStatus.INTERVIEW),
        (lt, open_jobs[1],  "React + Node.js experience. CS graduate.",                        ApplicationStatus.INTERVIEW),
        (lt, open_jobs[7],  "SQL + pandas. Available part-time weekends.",                     ApplicationStatus.PENDING),
        (lt, open_jobs[2],  "2yr React, TypeScript proficient.",                               ApplicationStatus.REVIEWING),
        (lh, open_jobs[6],  "3rd-year IT, eager to learn enterprise dev at FPT.",              ApplicationStatus.REJECTED),
        (lh, open_jobs[24], "Interested in logistics tech and route optimization.",            ApplicationStatus.PENDING),
        (pa, open_jobs[12], "TensorFlow + PyTorch, GPA 3.9, top ML student.",                 ApplicationStatus.INTERVIEW),
        (pa, open_jobs[1],  "Python + AI/ML background, want to grow full-stack.",            ApplicationStatus.REVIEWING),
        (pa, open_jobs[23], "High-performance Python experience. Love e-commerce scale.",     ApplicationStatus.PENDING),
        (vk, open_jobs[0],  "Learning Python. Would love to grow at TechViet.",               ApplicationStatus.PENDING),
        (vk, open_jobs[4],  "Strong SQL. Interested in database administration.",             ApplicationStatus.REVIEWING),
        (nt, open_jobs[17], "Flutter + RN, 2 apps published on App Store.",                   ApplicationStatus.INTERVIEW),
        (nt, open_jobs[10], "Cross-platform mobile, RN for 1.5 years.",                       ApplicationStatus.ACCEPTED),
        (lm, open_jobs[7],  "Data science background, SQL expert, Tableau certified.",        ApplicationStatus.ACCEPTED),
        (lm, open_jobs[14], "1yr data engineering, Spark and Airflow.",                       ApplicationStatus.REVIEWING),
        (lm, open_jobs[22], "Python + pandas. Behavioral data analysis experience.",          ApplicationStatus.PENDING),
        (pl, open_jobs[15], "CTF player, OWASP Top 10. Passionate about security.",           ApplicationStatus.INTERVIEW),
        (pl, open_jobs[0],  "Python backend + security expertise combination.",               ApplicationStatus.WITHDRAWN),
    ]

    for i, (student, job, cover, status) in enumerate(apps_data):
        app = Application(student_id=student.id, job_id=job.id,
                          cover_letter=cover, status=status,
                          applied_at=datetime.utcnow() - timedelta(days=len(apps_data)-i))
        db.add(app); db.commit(); db.refresh(app)
        db.add(ApplicationStatusLog(application_id=app.id, old_status=None,
                                    new_status=status, changed_by=coord_user.id,
                                    note="Set by seed"))
        db.commit()
    print(f"✅ {len(apps_data)} applications created")

    # ── SUMMARY ───────────────────────────────────────────
    print("\n" + "="*58)
    print("🎉 Seed completed! Pagination now testable (25 OPEN jobs)")
    print("="*58)
    print("\n  [Coordinator]  admin@studenttrack.com / admin123")
    print("\n  [Companies]    password: company123")
    for email, name, *_ in companies_raw:
        print(f"    {email:<33} {name}")
    print("\n  [Students]     password: student123")
    for email, name, *_ in students_raw:
        print(f"    {email:<42} {name}")
    print("="*58)
    db.close()


if __name__ == "__main__":
    seed()