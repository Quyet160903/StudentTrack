# StudentTrack — Internship & Career Management Portal

A full-stack web application that helps universities manage student internship placements and post-graduation employment tracking. Built as a portfolio project to demonstrate Python backend engineering with FastAPI.

---

## Features

### Three Role-Based Dashboards

**Student**
- Browse and search paginated open job postings (filter by type, keyword)
- Apply to jobs with cover letter and resume URL
- Track application status in real time
- View full status change history (timeline) for each application
- Withdraw pending applications
- Manage personal profile (GPA, major, graduation year, resume, bio)

**Company**
- Create and manage job postings through an approval workflow
- Resubmit rejected jobs after editing
- View applicants per job, update application status
- View full status change history per applicant
- Browse all open jobs from other companies
- Manage company profile

**Coordinator (Admin)**
- Overview dashboard — total students, companies, pending jobs, applications, accepted count
- Approve or reject pending job postings (with optional rejection note)
- View and manage all students, companies, jobs, and applications
- View full audit trail for any application
- Update any application status directly

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Auth | JWT — access token + refresh token rotation |
| Password hashing | bcrypt via passlib |
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
│   │   │   ├── config.py          ← env vars via pydantic-settings
│   │   │   ├── security.py        ← JWT + bcrypt helpers
│   │   │   └── deps.py            ← FastAPI dependencies (require_student, etc.)
│   │   ├── db/
│   │   │   └── database.py        ← SQLAlchemy engine + session
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── student.py
│   │   │   ├── company.py
│   │   │   ├── coordinator.py
│   │   │   ├── job_posting.py
│   │   │   ├── application.py
│   │   │   ├── application_log.py ← audit trail for status changes
│   │   │   └── refresh_token.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── job.py
│   │   │   ├── application.py
│   │   │   ├── application_log.py
│   │   │   ├── student.py
│   │   │   ├── company.py
│   │   │   └── pagination.py      ← generic PaginatedResponse[T]
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
        ├── api.js            ← fetch wrapper with JWT header
        └── auth.js           ← token helpers
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (running locally)
- VS Code with **Live Server** extension (for the frontend)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/studenttrack.git
cd studenttrack
```

### 2. Set up Python environment

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

Seed creates **30 job postings** (25 OPEN — enough to test pagination across 3 pages), 8 students, 5 companies, and 20 applications with varied statuses.

### 7. Start the backend

```bash
uvicorn app.main:app --reload
```

- API base URL: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

### 8. Open the frontend

Open `frontend/pages/index.html` with VS Code **Live Server**.

---

## Seed Accounts

### Coordinator
| Email | Password |
|---|---|
| admin@studenttrack.com | admin123 |

### Companies — password: `company123`
| Email | Company |
|---|---|
| hr@techviet.com | TechViet Solutions |
| recruit@fpt.com | FPT Software |
| jobs@vingroup.net | VinGroup Technology |
| talent@momo.vn | MoMo E-Wallet |
| careers@tiki.vn | Tiki Corporation |

### Students — password: `student123`
| Email | Name |
|---|---|
| minh.nguyen@student.edu.vn | Nguyen Thanh Minh |
| linh.tran@student.edu.vn | Tran Thi Linh |
| huy.le@student.edu.vn | Le Van Huy |
| an.pham@student.edu.vn | Pham Thi An |
| khoa.vo@student.edu.vn | Vo Minh Khoa |
| tuan.nguyen@student.edu.vn | Nguyen Duc Tuan |
| mai.le@student.edu.vn | Le Thi Mai |
| long.pham@student.edu.vn | Pham Hoang Long |

> ⚠️ Change all passwords before deploying to production.

---

## API Reference

All paginated endpoints accept `?page=1&page_size=N` (max `page_size=100`) and return:

```json
{
  "items": [...],
  "total": 47,
  "page": 2,
  "page_size": 9,
  "total_pages": 6
}
```

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/register` | Register student or company | Public |
| POST | `/auth/login` | Login — returns JWT access + refresh token | Public |
| POST | `/auth/token` | Login via Swagger UI (form-data) | Public |
| POST | `/auth/refresh` | Refresh access token, rotate refresh token | Public |

### Jobs
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/jobs/` | All OPEN jobs, paginated | Public |
| GET | `/jobs/{id}` | Job detail | Public |
| GET | `/jobs/my` | My company's jobs, paginated | Company |
| GET | `/jobs/all` | All jobs all statuses, paginated | Coordinator |
| GET | `/jobs/pending` | Pending approval jobs, paginated | Coordinator |
| POST | `/jobs/` | Create job (auto status: `pending`) | Company |
| PUT | `/jobs/{id}` | Update job (smart status transitions) | Company |
| POST | `/jobs/{id}/resubmit` | Resubmit rejected job for re-approval | Company |
| PUT | `/jobs/{id}/approve` | Approve pending job | Coordinator |
| PUT | `/jobs/{id}/reject` | Reject pending job with note | Coordinator |
| DELETE | `/jobs/{id}` | Delete job (cascades to applications) | Company |

### Applications
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/applications/` | Apply to a job | Student |
| GET | `/applications/my` | My applications | Student |
| GET | `/applications/job/{job_id}` | Applicants for a job | Company |
| GET | `/applications/all` | All applications, paginated + `?status=` filter | Coordinator |
| GET | `/applications/{id}/logs` | Full status change history | Student / Company / Coordinator |
| PUT | `/applications/{id}/status` | Update status | Company / Coordinator / Student (withdraw only) |

### Students
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/students/` | All students | Coordinator |
| GET | `/students/profile` | My profile | Student |
| PUT | `/students/profile` | Update my profile | Student |

### Companies
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/companies/` | All companies | Coordinator |
| GET | `/companies/profile` | My profile | Company |
| PUT | `/companies/profile` | Update my profile | Company |

---

## Authentication Flow

```
Register  →  POST /auth/register  →  UserResponse
Login     →  POST /auth/login     →  { access_token, refresh_token }
API call  →  Authorization: Bearer <access_token>
Expired   →  POST /auth/refresh   →  new access_token + new refresh_token
                                      old refresh token is revoked (rotation)
```

---

## Job Posting Status Flow

```
Company creates job
        ↓
    PENDING ◄─────────────────────────────────────────────┐
        │  Coordinator reviews                             │
        ├──► APPROVED                                      │
        │        │                                         │
        │        ▼                                         │
        │      OPEN ◄────► CLOSED   (no re-approval)      │
        │        │                                         │
        │        └── company edits content ────────────────┘
        │                                   (auto reset to PENDING)
        └──► REJECTED
                 │
                 └── company edits & resubmits ────────────┘
```

| From | To | Who | Notes |
|---|---|---|---|
| — | `pending` | Company | On create |
| `pending` | `approved` | Coordinator | |
| `pending` | `rejected` | Coordinator | Rejection note stored on job |
| `rejected` | `pending` | Company | After editing + resubmit |
| `approved` | `open` | Company | Makes job visible to students |
| `open` | `closed` | Company | Hides from students temporarily |
| `closed` | `open` | Company | Reopen — no re-approval needed |
| `open` / `closed` | `pending` | System | Auto-reset when company edits job content |

> Only `open` jobs appear in the public listing (`GET /jobs/`).

---

## Application Status Flow

```
Student applies
      ↓
   PENDING → REVIEWING → INTERVIEW → ACCEPTED
                                  ↘ REJECTED
   (student can withdraw at any active stage → WITHDRAWN)
```

Every status change is automatically written to `application_status_logs` with:
- Old status → new status
- Who changed it (user ID, full name, role)
- Timestamp
- Optional note

The full history is accessible via `GET /applications/{id}/logs` and displayed as a color-coded timeline in the UI for all three roles.

---

## Role Permissions

| Action | Student | Company | Coordinator |
|---|---|---|---|
| Browse open jobs | ✅ | ✅ | ✅ |
| Apply to job | ✅ | ❌ | ❌ |
| Withdraw own application | ✅ | ❌ | ❌ |
| View own application logs | ✅ | ❌ | ❌ |
| Create / edit / delete job | ❌ | ✅ own only | ❌ |
| Resubmit rejected job | ❌ | ✅ own only | ❌ |
| View applicants + their logs | ❌ | ✅ own jobs | ✅ all |
| Update application status | ❌ | ✅ own jobs | ✅ all |
| Approve / reject job | ❌ | ❌ | ✅ |
| View all students / companies | ❌ | ❌ | ✅ |
| Self-register | ✅ | ✅ | ❌ seeded only |

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `SECRET_KEY` | JWT signing secret — use a long random string in production | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime (default: 30) | |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime (default: 7) | |

---

## What This Project Demonstrates

- **FastAPI** — routing, dependency injection, Swagger UI, lifespan events
- **SQLAlchemy 2.0** — ORM models, relationships, cascade deletes, enum columns
- **Alembic** — migration workflow including enum and FK constraint changes
- **Pydantic v2** — request/response validation, generic schemas (`PaginatedResponse[T]`)
- **JWT authentication** — access + refresh token rotation, role-based route guards
- **Service-layer architecture** — routers stay thin, all business logic lives in services
- **Offset pagination** — generic `PaginationParams` dependency reused across all listing endpoints
- **Audit trail** — every application status change logged with actor name, role, and timestamp
- **Approval workflow** — multi-step job posting flow with smart automatic status transitions
- **Vanilla JS ES Modules** — no framework, native fetch API, JWT token management, dynamic UI rendering