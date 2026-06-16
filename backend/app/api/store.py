import json
from pathlib import Path
from typing import Any, cast
from uuid import uuid4
from app.apply.tracker import Application
from app.db.models import CareerProfile, JobPosting, Resume

RESUMES: dict[str, Resume] = {}
JOBS: dict[str, JobPosting] = {}
APPLICATIONS: dict[str, Application] = {}
DATA_DIR = Path("data")


def load_store() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    _load_resumes()
    _load_jobs()
    _load_applications()


def save_resume(resume: Resume) -> str:
    resume_id = f"res_{uuid4().hex[:12]}"
    RESUMES[resume_id] = resume
    _write_json("resumes.json", {key: value.model_dump(mode="json") for key, value in RESUMES.items()})
    return resume_id


def save_jobs(jobs: list[JobPosting]) -> None:
    for job in jobs:
        JOBS[job.id] = job
    _write_json("jobs.json", {key: value.model_dump(mode="json") for key, value in JOBS.items()})


def save_application(application: Application) -> Application:
    APPLICATIONS[application.job_id] = application
    _write_json(
        "applications.json",
        {key: value.model_dump(mode="json") for key, value in APPLICATIONS.items()},
    )
    return application


def profile_from_resume(resume: Resume) -> CareerProfile:
    return CareerProfile(
        contact=resume.contact,
        experiences=resume.experience,
        education=resume.education,
        projects=resume.projects,
        skills=resume.skills,
        preferences={"remote": True, "level": "mid"},
    )


def _load_resumes() -> None:
    for key, value in _read_json("resumes.json").items():
        RESUMES[key] = Resume.model_validate(value)


def _load_jobs() -> None:
    for key, value in _read_json("jobs.json").items():
        JOBS[key] = JobPosting.model_validate(value)


def _load_applications() -> None:
    for key, value in _read_json("applications.json").items():
        APPLICATIONS[key] = Application.model_validate(value)


def _read_json(filename: str) -> dict[str, Any]:
    path = DATA_DIR / filename
    if not path.exists():
        return {}
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _write_json(filename: str, payload: dict[str, Any]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")
