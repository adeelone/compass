import re
from dataclasses import dataclass
from app.db.models import Resume


@dataclass(frozen=True)
class ContentFinding:
    bullet: str
    issue: str
    rewrite: str
    source: str


ACTION_VERBS = {"built", "led", "reduced", "increased", "launched", "designed", "automated", "improved"}


def score_content(resume: Resume) -> tuple[int, list[str], list[ContentFinding]]:
    bullets = [bullet for exp in resume.experience for bullet in exp.bullets]
    if not bullets:
        return 45, [], [ContentFinding("", "No accomplishment bullets found.", "Add bullets with action, scope, and measured outcome.", "deterministic:bullet-presence")]
    quantified = sum(bool(re.search(r"\d|%|\$|k\b|m\b", bullet.lower())) for bullet in bullets)
    verbs = sum(bullet.split(" ", 1)[0].lower() in ACTION_VERBS for bullet in bullets if bullet)
    score = min(100, 45 + round((quantified / len(bullets)) * 35) + round((verbs / len(bullets)) * 20))
    best = sorted(bullets, key=lambda item: (bool(re.search(r"\d|%|\$", item)), len(item)), reverse=True)[:5]
    findings = [
        ContentFinding(bullet, "Missing quantified impact.", f"{bullet.rstrip('.')} with a measurable business or user outcome.", "deterministic:metric-regex")
        for bullet in bullets
        if not re.search(r"\d|%|\$", bullet)
    ][:5]
    return score, best, findings

