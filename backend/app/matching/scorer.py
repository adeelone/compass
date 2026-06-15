from dataclasses import dataclass
from app.db.models import CareerProfile, JobPosting


@dataclass(frozen=True)
class MatchReason:
    label: str
    points: int
    evidence: str
    source: str


def score_job(profile: CareerProfile, job: JobPosting) -> tuple[int, list[MatchReason], list[str]]:
    skill_names = {skill.name.lower() for skill in profile.skills}
    description = job.description.lower()
    matched = sorted(skill for skill in skill_names if skill in description)
    missing = [term for term in ["python", "react", "postgres", "fastapi"] if term in description and term not in matched]
    skill_points = min(55, len(matched) * 14)
    remote_points = 15 if job.is_remote and profile.preferences.get("remote") in (True, "remote", "hybrid") else 5
    level_points = 15 if job.seniority in (None, profile.preferences.get("level"), "mid") else 8
    score = min(100, skill_points + remote_points + level_points + 15)
    reasons = [
        MatchReason("Skill overlap", skill_points, ", ".join(matched) or "No direct skill overlap found.", "profile.skills + job.description"),
        MatchReason("Location fit", remote_points, "Remote-compatible posting." if job.is_remote else "Location requires review.", "profile.preferences.remote + job.locations"),
        MatchReason("Level fit", level_points, f"Posting seniority: {job.seniority or 'unspecified'}.", "job.seniority"),
    ]
    return score, reasons, missing

