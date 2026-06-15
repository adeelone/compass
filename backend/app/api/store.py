from uuid import uuid4
from app.db.models import CareerProfile, JobPosting, Resume

RESUMES: dict[str, Resume] = {}
JOBS: dict[str, JobPosting] = {}


def save_resume(resume: Resume) -> str:
    resume_id = f"res_{uuid4().hex[:12]}"
    RESUMES[resume_id] = resume
    return resume_id


def save_jobs(jobs: list[JobPosting]) -> None:
    for job in jobs:
        JOBS[job.id] = job


def profile_from_resume(resume: Resume) -> CareerProfile:
    return CareerProfile(
        contact=resume.contact,
        experiences=resume.experience,
        education=resume.education,
        projects=resume.projects,
        skills=resume.skills,
        preferences={"remote": True, "level": "mid"},
    )
