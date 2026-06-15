from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from app.api.store import JOBS, RESUMES, profile_from_resume, save_jobs, save_resume
from app.db.models import CareerProfile, Contact, JobPosting, Skill
from app.jobs.providers.registry import get_providers
from app.matching.gap_closer import recommend_resources
from app.matching.scorer import MatchReason, score_job
from app.profile.completeness import completeness
from app.resume.ats_rules import evaluate_ats
from app.resume.content_scorer import score_content
from app.resume.parser import parse_resume_text

router = APIRouter()


class ResumeTextRequest(BaseModel):
    text: str
    filename: str = "resume.pdf"


class MatchRequest(BaseModel):
    profile: CareerProfile
    query: str = "software"
    location: str | None = None


class StoredMatchRequest(BaseModel):
    resume_id: str
    job_id: str


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/resume/analyze")
def analyze_resume(payload: ResumeTextRequest) -> dict[str, object]:
    resume = parse_resume_text(payload.text)
    ats_score, ats_rules = evaluate_ats(resume, payload.filename)
    content_score, best, findings = score_content(resume)
    return {
        "resume": resume.model_dump(mode="json"),
        "ats_score": ats_score,
        "ats_rules": [rule.__dict__ for rule in ats_rules],
        "content_score": content_score,
        "best_points": best,
        "weak_spots": [finding.__dict__ for finding in findings],
    }


@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)) -> dict[str, object]:
    raw = await file.read()
    text = raw.decode("utf-8", errors="ignore")
    resume = parse_resume_text(text)
    ats_score, _ats_rules = evaluate_ats(resume, file.filename or "resume.pdf")
    content_score, _best, _findings = score_content(resume)
    resume_id = save_resume(resume)
    return {
        "resume_id": resume_id,
        "ats_score": ats_score,
        "content_score": content_score,
        "parsed_sections": {
            "work": [item.model_dump(mode="json") for item in resume.experience],
            "education": [item.model_dump(mode="json") for item in resume.education],
            "skills": [item.model_dump(mode="json") for item in resume.skills],
        },
    }


@router.get("/jobs")
async def jobs(query: str = "python intern", location: str | None = None) -> dict[str, object]:
    provider = get_providers()[0]
    postings = await provider.search(query, location)
    save_jobs(postings)
    profile = _default_profile()
    results = []
    for job in postings:
        score, reasons, missing = score_job(profile, job)
        results.append(_job_payload(job, score, reasons, missing))
    return {"results": results}


@router.post("/jobs/match")
async def match_jobs(payload: MatchRequest) -> dict[str, object]:
    provider = get_providers()[0]
    jobs = await provider.search(payload.query, payload.location)
    save_jobs(jobs)
    scored = []
    for job in jobs:
        score, reasons, missing = score_job(payload.profile, job)
        scored.append(_job_payload(job, score, reasons, missing))
    return {"results": scored}


@router.post("/match")
def match_stored(payload: StoredMatchRequest) -> dict[str, object]:
    resume = RESUMES.get(payload.resume_id)
    job = JOBS.get(payload.job_id)
    if resume is None:
        raise HTTPException(status_code=404, detail="resume_id not found")
    if job is None:
        raise HTTPException(status_code=404, detail="job_id not found")
    score, reasons, missing = score_job(profile_from_resume(resume), job)
    result = _job_payload(job, score, reasons, missing)
    return {
        "score": result["score"],
        "matched_keywords": result["matched_keywords"],
        "missing_keywords": result["missing_keywords"],
        "gap_closers": result["gap_closers"],
        "why": result["why"],
    }


@router.post("/profile/completeness")
def profile_completeness(profile: CareerProfile) -> dict[str, object]:
    score, next_steps = completeness(profile)
    return {"score": score, "next_steps": next_steps}


def _default_profile() -> CareerProfile:
    resume = next(iter(RESUMES.values()), None)
    if resume:
        return profile_from_resume(resume)
    return CareerProfile(
        contact=Contact(name="Sample Candidate", email="sample@example.com"),
        skills=[Skill(name="Python"), Skill(name="FastAPI")],
        preferences={"remote": True, "level": "mid"},
    )


def _job_payload(
    job: JobPosting,
    score: int,
    reasons: list[MatchReason],
    missing: list[str],
) -> dict[str, object]:
    matched = sorted(
        {word for reason in reasons for word in reason.evidence.lower().replace(",", " ").split()}
        & {"python", "fastapi", "react", "postgres", "postgresql"}
    )
    return {
        "job": job.model_dump(mode="json"),
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "source": {"id": job.source, "kind": job.source_kind.value, "url": job.apply_url},
        "source_attribution": f"{job.source}:{job.raw_hash}",
        "why": [reason.__dict__ for reason in reasons],
        "gap_closers": recommend_resources(missing),
    }
