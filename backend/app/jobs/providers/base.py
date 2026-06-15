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

