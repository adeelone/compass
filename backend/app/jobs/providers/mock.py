from datetime import datetime
from app.db.models import JobPosting, JobSourceKind
from app.jobs.providers.base import JobProvider, ProviderMetadata


class MockProvider(JobProvider):
    metadata = ProviderMetadata(
        id="mock",
        kind=JobSourceKind.official_api,
        rate_limit_per_minute=120,
        cache_ttl_seconds=900,
        supported_filters=["query", "location", "remote"],
        tos_notes="Synthetic provider for tests and local development.",
    )

    async def search(self, query: str, location: str | None = None) -> list[JobPosting]:
        return [
            JobPosting(
                id="mock-1",
                title=f"{query.title()} Engineer",
                company="Example Systems",
                locations=[location or "Remote"],
                is_remote=True,
                employment_type="full-time",
                seniority="mid",
                posted_at=datetime.utcnow(),
                description="Build Python, FastAPI, PostgreSQL, React, and data pipelines for career products.",
                apply_url="https://example.com/jobs/mock-1",
                source=self.metadata.id,
                source_kind=self.metadata.kind,
                raw_hash="mock-1",
            )
        ]

