from app.db.models import JobPosting
from app.jobs.normalize import normalized_key


def dedupe_jobs(jobs: list[JobPosting]) -> list[JobPosting]:
    seen: set[str] = set()
    deduped: list[JobPosting] = []
    for job in jobs:
        key = normalized_key(job.company, job.title, job.locations[0] if job.locations else "")
        if key in seen:
            continue
        seen.add(key)
        deduped.append(job)
    return deduped


def dedupe_exact_source(jobs: list[JobPosting]) -> list[JobPosting]:
    seen: set[str] = set()
    result: list[JobPosting] = []
    for job in jobs:
        key = f"{job.source}:{job.raw_hash}"
        if key in seen:
            continue
        seen.add(key)
        result.append(job)
    return result
