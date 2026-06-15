import asyncio
from app.db.models import CareerProfile, Contact, Skill
from app.jobs.providers.mock import MockProvider
from app.matching.gap_closer import recommend_resources
from app.matching.scorer import score_job


def test_matching_returns_sourced_reasons() -> None:
    asyncio.run(_run())


async def _run() -> None:
    profile = CareerProfile(
        contact=Contact(name="Ada Example", email="ada@example.com"),
        headline="Backend engineer",
        skills=[Skill(name="Python"), Skill(name="FastAPI")],
        preferences={"remote": True, "level": "mid"},
    )
    job = (await MockProvider().search("backend"))[0]
    score, reasons, missing = score_job(profile, job)
    assert score >= 50
    assert all(reason.source for reason in reasons)
    assert "react" in missing
    assert recommend_resources(missing)["react"]
