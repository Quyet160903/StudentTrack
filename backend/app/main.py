from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import auth_router
from app.api.jobs import job_router
from app.api.applications import application_router
from app.api.companies import company_router
from app.api.students import student_router

app = FastAPI(
    title="StudenTrack API",
    description="Intership & Career Management Portal",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(job_router)
app.include_router(application_router)
app.include_router(company_router)
app.include_router(student_router)

@app.get("/")
def root():
    return {"messages": "StudentTrack API is running"}