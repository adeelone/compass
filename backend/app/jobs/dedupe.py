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

