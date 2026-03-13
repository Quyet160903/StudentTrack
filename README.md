# StudentTrack — Internship & Career Management Portal

A full-stack web application that helps universities manage student internship placements and post-graduation employment tracking. Built with **Python FastAPI** backend and **Vanilla HTML/CSS/JS** frontend.

---

## Features

### Three Role-Based Dashboards

**Student**
- Browse and search all open job postings
- Apply with cover letter and resume URL
- Track application status in real time
- Withdraw pending applications
- Manage personal profile (GPA, major, resume, bio)

**Company**
- Create and manage own job postings
- Job posting approval flow — new jobs are submitted for coordinator review before going live
- Resubmit rejected jobs after editing
- View applicants per job and update application status
- Browse all open jobs from other companies (read-only)
- Manage company profile

**Coordinator (Admin)**
- Overview dashboard with key stats (students, companies, jobs, applications, accepted)
- Approve or reject pending job postings with optional rejection note
- View all students, companies, jobs, and applications across the platform
- Update any application status

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Auth | JWT (access + refresh token rotation) |
| Password | bcrypt via passlib |
| Validation | Pydantic v2 |
| Frontend | Vanilla HTML, CSS, JavaScript (ES Modules) |

---

## Project Structure

```
studenttrack/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── jobs.py
│   │   │   ├── applications.py
│   │   │   ├── students.py
│   │   │   └── companies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── deps.py
│   │   ├── db/
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── student.py
│   │   │   ├── company.py
│   │   │   ├── coordinator.py
│   │   │   ├── job_posting.py
│   │   │   ├── application.py
│   │   │   ├── application_log.py
│   │   │   └── refresh_token.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── job.py
│   │   │   ├── application.py
│   │   │   ├── student.py
│   │   │   └── company.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── job_service.py
│   │   │   ├── application_service.py
│   │   │   ├── student_service.py
│   │   │   └── company_service.py
│   │   └── main.py
│   ├── migrations/
│   ├── seed.py
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── pages/
    │   ├── index.html        ← Login / Register
    │   ├── student.html      ← Student Dashboard
    │   ├── company.html      ← Company Dashboard
    │   └── coordinator.html  ← Coordinator Dashboard
    ├── css/
    │   └── main.css
    └── js/
        ├── api.js
        └── auth.js
```

---

## Database Schema

```
users                   — base auth table (email, password_hash, role)
students                — student profile (gpa, major, student_id, bio)
companies               — company profile (name, location, contact)
coordinators            — coordinator profile (department)
job_postings            — job listings (title, type, salary, status, deadline, rejection_note)
applications            — student applications (status, cover_letter, resume_url)
application_status_logs — full audit trail for every status change
refresh_tokens          — JWT refresh token rotation storage
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- VS Code with Live Server extension (for frontend)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/studenttrack.git
cd studenttrack
```

### 2. Setup Python environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/studenttrack
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 4. Create the database

```sql
CREATE DATABASE studenttrack;
```

### 5. Run database migrations

```bash
# Windows — set PYTHONPATH first
set PYTHONPATH=C:\path\to\studenttrack\backend
alembic upgrade head

# macOS / Linux
alembic upgrade head
```

### 6. Seed sample data

```bash
python seed.py
```

This creates all sample accounts:

| Role | Email | Password |
|---|---|---|
| Coordinator | admin@studenttrack.com | admin123 |
| Company | hr@techviet.com | company123 |
| Company | recruit@fpt.com | company123 |
| Company | jobs@vingroup.net | company123 |
| Student | minh.nguyen@student.edu.vn | student123 |
| Student | linh.tran@student.edu.vn | student123 |
| Student | huy.le@student.edu.vn | student123 |
| Student | an.pham@student.edu.vn | student123 |
| Student | khoa.vo@student.edu.vn | student123 |

> ⚠️ Change passwords after first login in production.

### 7. Start the backend server

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

### 8. Open the frontend

Open `frontend/pages/index.html` with VS Code Live Server.

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/register` | Register student or company | Public |
| POST | `/auth/login` | Login — returns JWT tokens | Public |
| POST | `/auth/token` | Login via Swagger UI (form-data) | Public |
| POST | `/auth/refresh` | Refresh access token | Public |

### Jobs
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/jobs/` | List all open jobs | Public |
| GET | `/jobs/my` | List my company's jobs (all statuses) | Company |
| GET | `/jobs/all` | List all jobs regardless of status | Coordinator |
| GET | `/jobs/pending` | List jobs pending approval | Coordinator |
| GET | `/jobs/{id}` | Get job detail | Public |
| POST | `/jobs/` | Create job posting (auto status: pending) | Company |
| PUT | `/jobs/{id}` | Update job posting | Company |
| POST | `/jobs/{id}/resubmit` | Resubmit rejected job for re-approval | Company |
| PUT | `/jobs/{id}/approve` | Approve a pending job | Coordinator |
| PUT | `/jobs/{id}/reject` | Reject a pending job with note | Coordinator |
| DELETE | `/jobs/{id}` | Delete job posting | Company |

### Applications
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/applications/` | Apply to a job | Student |
| GET | `/applications/my` | Get my applications | Student |
| GET | `/applications/job/{job_id}` | Get applicants for a job | Company |
| PUT | `/applications/{id}/status` | Update application status | Company / Coordinator / Student (withdraw only) |
| GET | `/applications/all` | Get all applications | Coordinator |

### Students
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/students/` | List all students | Coordinator |
| GET | `/students/profile` | Get my profile | Student |
| PUT | `/students/profile` | Update my profile | Student |

### Companies
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/companies/` | List all companies | Coordinator |
| GET | `/companies/profile` | Get my profile | Company |
| PUT | `/companies/profile` | Update my profile | Company |

---

## Authentication Flow

```
Register  →  POST /auth/register  →  returns UserResponse
Login     →  POST /auth/login     →  returns access_token + refresh_token
API call  →  Authorization: Bearer <access_token>
Expired   →  POST /auth/refresh   →  returns new access_token + new refresh_token
                                      (old refresh token is revoked)
```

Token rotation is implemented — every refresh invalidates the old refresh token and issues a fresh pair.

---

## Job Posting Flow

```
Company creates job
        ↓
    PENDING  ──────────────────────────────────────────────────────┐
        ↓  (Coordinator reviews)                                    │
   APPROVED ──── REJECTED (with note)                              │
        ↓              ↓                                            │
      OPEN      Company edits & resubmits ──────────────────────────┘
        ↓
     CLOSED  ──── (reopen, no re-approval needed)  ──────── OPEN
        ↓
   Company edits content
        ↓
    PENDING  (requires re-approval since content changed)
```

**Status transition rules:**

| From | To | Who | Condition |
|---|---|---|---|
| — | `PENDING` | Company | On create |
| `PENDING` | `APPROVED` | Coordinator | — |
| `PENDING` | `REJECTED` | Coordinator | With optional note |
| `REJECTED` | `PENDING` | Company | Resubmit after editing |
| `APPROVED` | `OPEN` | Company | Make visible to students |
| `OPEN` | `CLOSED` | Company | Hide temporarily |
| `CLOSED` | `OPEN` | Company | Reopen — **no re-approval needed** |
| `OPEN` / `CLOSED` | `PENDING` | Company | Auto-reset when content is edited |

> Only `OPEN` jobs appear in the public listing (`GET /jobs/`).
> Editing content on a live (`OPEN`) or `CLOSED` job automatically resets it to `PENDING` for coordinator re-approval.

---

## Application Status Flow

```
PENDING → REVIEWING → INTERVIEW → ACCEPTED
                               ↘ REJECTED
PENDING → WITHDRAWN  (student can withdraw at any active stage)
```

Every status change is automatically logged to `application_status_logs` with timestamp and the user who made the change.

---

## Role Permissions

| Action | Student | Company | Coordinator |
|---|---|---|---|
| Browse open jobs | ✅ | ✅ | ✅ |
| View job detail | ✅ | ✅ | ✅ |
| Apply to job | ✅ | ❌ | ❌ |
| Withdraw own application | ✅ | ❌ | ❌ |
| Create job posting | ❌ | ✅ | ❌ |
| Edit / delete own job | ❌ | ✅ (own only) | ❌ |
| Resubmit rejected job | ❌ | ✅ (own only) | ❌ |
| Approve / reject job | ❌ | ❌ | ✅ |
| View own job applicants | ❌ | ✅ (own only) | ✅ (all) |
| Update application status | ❌ | ✅ (own jobs) | ✅ (all) |
| View all students | ❌ | ❌ | ✅ |
| View all companies | ❌ | ❌ | ✅ |
| View all jobs | ❌ | ❌ | ✅ |
| View all applications | ❌ | ❌ | ✅ |
| Self-register | ✅ | ✅ | ❌ (seeded only) |

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | required |
| `SECRET_KEY` | JWT signing secret | required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | 7 |

---

## Built With

This project was built as a portfolio project to demonstrate:

- Python backend development with FastAPI
- Clean service-layer architecture (router → service → model)
- Relational database design with SQLAlchemy + Alembic migrations
- JWT authentication with refresh token rotation
- Role-based access control (RBAC)
- RESTful API design with Pydantic v2 validation
- Job approval workflow with audit trail
- Full-stack integration with Vanilla JS ES Modules frontend