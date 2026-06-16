from app.jobs.providers.base import JobProvider
from app.jobs.providers.mock import MockProvider
from app.jobs.providers.official import (
    AdzunaProvider,
    AshbyProvider,
    GreenhouseProvider,
    LeverProvider,
    RemotiveProvider,
    USAJobsProvider,
)


def get_providers() -> list[JobProvider]:
    return [
        MockProvider(),
        GreenhouseProvider(),
        LeverProvider(),
        AshbyProvider(),
        AdzunaProvider(),
        USAJobsProvider(),
        RemotiveProvider(),
    ]
