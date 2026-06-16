from app.db.models import JobSourceKind
from app.jobs.providers.base import ProviderMetadata, StaticProvider


class GreenhouseProvider(StaticProvider):
    metadata = ProviderMetadata(
        id="greenhouse",
        kind=JobSourceKind.official_api,
        rate_limit_per_minute=60,
        cache_ttl_seconds=900,
        supported_filters=["query", "location"],
        tos_notes="Uses public company board endpoints when configured.",
    )


class LeverProvider(StaticProvider):
    metadata = ProviderMetadata(
        id="lever",
        kind=JobSourceKind.official_api,
        rate_limit_per_minute=60,
        cache_ttl_seconds=900,
        supported_filters=["query", "location"],
        tos_notes="Uses public postings endpoints when configured.",
    )


class AshbyProvider(StaticProvider):
    metadata = ProviderMetadata(
        id="ashby",
        kind=JobSourceKind.official_api,
        rate_limit_per_minute=60,
        cache_ttl_seconds=900,
        supported_filters=["query", "location"],
        tos_notes="Uses public job board endpoints when configured.",
    )


class AdzunaProvider(StaticProvider):
    metadata = ProviderMetadata(
        id="adzuna",
        kind=JobSourceKind.partner_api,
        rate_limit_per_minute=30,
        cache_ttl_seconds=1800,
        supported_filters=["query", "location", "salary"],
        tos_notes="Requires user-supplied API credentials for live calls.",
    )


class USAJobsProvider(StaticProvider):
    metadata = ProviderMetadata(
        id="usajobs",
        kind=JobSourceKind.public_feed,
        rate_limit_per_minute=30,
        cache_ttl_seconds=1800,
        supported_filters=["query", "location"],
        tos_notes="Requires API key and attribution for live calls.",
    )


class RemotiveProvider(StaticProvider):
    metadata = ProviderMetadata(
        id="remotive",
        kind=JobSourceKind.public_feed,
        rate_limit_per_minute=60,
        cache_ttl_seconds=1800,
        supported_filters=["query", "remote"],
        tos_notes="Public API; respect documented rate limits.",
    )
