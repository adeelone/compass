import asyncio
from app.jobs.dedupe import dedupe_jobs
from app.jobs.providers.mock import MockProvider


def test_mock_provider_and_dedupe() -> None:
    asyncio.run(_run())


async def _run() -> None:
    provider = MockProvider()
    jobs = await provider.search("backend", "Remote")
    assert provider.metadata.tos_notes
    assert len(dedupe_jobs(jobs + jobs)) == 1
