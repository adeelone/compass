from pathlib import Path
from app.apply.tracker import Application, ApplicationStatus
from app.auth.sessions import create_session
from app.core.circuit_breaker import CircuitBreaker
from app.core.rate_limit import TokenBucket
from app.db.models import CareerProfile, Contact, Experience, JobPosting, JobSourceKind, Skill
from app.embeddings.provider import MockEmbeddingProvider
from app.jobs.index import search_jobs
from app.llm.provider import MockLLMProvider
from app.notify.digest import build_digest
from app.profile.completeness import completeness, public_profile
from app.resume.extract import extract_resume_text
from app.resume.rewrite import rewrite_bullet
from app.search.hybrid import hybrid_rank
from app.storage.local import LocalStorage
from app.tailoring.resume import tailored_summary
import asyncio


def test_core_services_and_helpers() -> None:
    bucket = TokenBucket(rate_per_second=1, burst=1)
    assert bucket.allow()
    assert not bucket.allow()

    breaker = CircuitBreaker(failure_threshold=1)
    assert breaker.allow()
    breaker.record_failure()
    assert not breaker.allow()
    breaker.record_success()
    assert breaker.allow()

    session = create_session("user@example.com")
    assert session.subject == "user@example.com"

    app = Application(job_id="job-1", status=ApplicationStatus.applied)
    assert app.status == ApplicationStatus.applied

    store = LocalStorage(Path("test-output"))
    assert store.put_text("notes/a.txt", "hello").read_text(encoding="utf-8") == "hello"


def test_profile_tailoring_digest_and_ai_mocks() -> None:
    job = JobPosting(
        id="job-1",
        title="Python Backend Intern",
        company="Example Systems",
        description="Python FastAPI PostgreSQL role",
        apply_url="https://example.com/jobs/1",
        source="mock",
        source_kind=JobSourceKind.official_api,
        raw_hash="job-1",
    )
    profile = CareerProfile(
        contact=Contact(name="Ada Example", email="ada@example.com"),
        headline="Backend intern",
        experiences=[Experience(company="Campus Tools Lab", title="Backend Intern")],
        skills=[Skill(name="Python"), Skill(name="FastAPI")],
        preferences={"remote": True},
    )
    score, next_steps = completeness(profile)
    assert score >= 75
    assert "Ada Example" in tailored_summary(profile, job)
    assert "Python Backend Intern" in build_digest([job])
    assert search_jobs([job], "python")
    assert hybrid_rank([job], "fastapi") == [job]
    assert len(rewrite_bullet("Built APIs")) == 3
    assert extract_resume_text("resume.txt", b"Ada Example")[0] == "Ada Example"
    assert public_profile(profile) == {"name": "Ada Example"}

    async def run_mocks() -> None:
        assert await MockEmbeddingProvider().embed("abc")
        result = await MockLLMProvider().complete_json("prompt", "schema")
        assert result["schema"] == "schema"

    asyncio.run(run_mocks())
