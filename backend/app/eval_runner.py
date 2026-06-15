from app.db.models import CareerProfile, Contact, Skill
from app.jobs.providers.mock import MockProvider
from app.matching.scorer import score_job
from app.resume.ats_rules import evaluate_ats
from app.resume.parser import parse_resume_text
import asyncio


async def main() -> None:
    resume = parse_resume_text("Ada Example\nada@example.com\nSkills\nPython, FastAPI\n- Built API used by 120 teams")
    ats_score, rules = evaluate_ats(resume)
    profile = CareerProfile(
        contact=Contact(name="Ada Example", email="ada@example.com"),
        skills=[Skill(name="Python"), Skill(name="FastAPI")],
        preferences={"remote": True},
    )
    job = (await MockProvider().search("backend"))[0]
    match_score, reasons, _missing = score_job(profile, job)
    assert ats_score >= 75
    assert all(rule.source for rule in rules)
    assert match_score >= 50
    assert all(reason.source for reason in reasons)
    print("eval passed: deterministic resume and match checks met thresholds")


if __name__ == "__main__":
    asyncio.run(main())

