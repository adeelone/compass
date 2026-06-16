from app.db.models import JobSourceKind
from app.jobs.providers.base import ProviderMetadata, StaticProvider


class MockProvider(StaticProvider):
    metadata = ProviderMetadata(
        id="mock",
        kind=JobSourceKind.official_api,
        rate_limit_per_minute=120,
        cache_ttl_seconds=900,
        supported_filters=["query", "location", "remote"],
        tos_notes="Synthetic provider for tests and local development.",
    )
