from app.jobs.providers.base import JobProvider
from app.jobs.providers.mock import MockProvider


def get_providers() -> list[JobProvider]:
    return [MockProvider()]

