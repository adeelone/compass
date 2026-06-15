from fastapi import APIRouter
from pydantic import BaseModel
from app.db.models import CareerProfile
from app.jobs.providers.registry import get_providers
from app.matching.gap_closer import recommend_resources
from app.matching.scorer import score_job
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


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/resume/analyze")
def analyze_resume(payload: ResumeTextRequest) -> dict:
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


@router.post("/jobs/match")
async def match_jobs(payload: MatchRequest) -> dict:
    provider = get_providers()[0]
    jobs = await provider.search(payload.query, payload.location)
    scored = []
    for job in jobs:
        score, reasons, missing = score_job(payload.profile, job)
        scored.append({
            "job": job.model_dump(mode="json"),
            "score": score,
            "why": [reason.__dict__ for reason in reasons],
            "missing_keywords": missing,
            "gap_closers": recommend_resources(missing),
        })
    return {"results": scored}


@router.post("/profile/completeness")
def profile_completeness(profile: CareerProfile) -> dict:
    score, next_steps = completeness(profile)
    return {"score": score, "next_steps": next_steps}

