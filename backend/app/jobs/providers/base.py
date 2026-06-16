from abc import ABC, abstractmethod
from dataclasses import dataclass
from app.db.models import JobPosting, JobSourceKind


@dataclass(frozen=True)
class ProviderMetadata:
    id: str
    kind: JobSourceKind
    rate_limit_per_minute: int
    cache_ttl_seconds: int
    supported_filters: list[str]
    tos_notes: str


class JobProvider(ABC):
    metadata: ProviderMetadata

    @abstractmethod
    async def search(self, query: str, location: str | None = None) -> list[JobPosting]:
        raise NotImplementedError


class StaticProvider(JobProvider):
    def _job(self, query: str, location: str | None = None) -> JobPosting:
        normalized = query.replace("+", " ")
        title = "Python Backend Intern" if "intern" in normalized.lower() else f"{normalized.title()} Engineer"
        return JobPosting(
            id=f"{self.metadata.id}-1",
            title=title,
            company=f"{self.metadata.id.title()} Example",
            locations=[location or "Remote"],
            is_remote=True,
            employment_type="internship" if "intern" in normalized.lower() else "full-time",
            seniority="intern" if "intern" in normalized.lower() else "mid",
            description=(
                "Build Python and FastAPI services with PostgreSQL, Redis, React dashboards, "
                "and data pipelines for career products."
            ),
            apply_url=f"https://example.com/{self.metadata.id}/jobs/1",
            source=self.metadata.id,
            source_kind=self.metadata.kind,
            raw_hash=f"{self.metadata.id}-1",
        )

    async def search(self, query: str, location: str | None = None) -> list[JobPosting]:
        return [self._job(query, location)]
