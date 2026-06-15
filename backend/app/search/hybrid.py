from app.db.models import JobPosting


def hybrid_rank(jobs: list[JobPosting], query: str) -> list[JobPosting]:
    lowered = query.lower()
    return sorted(jobs, key=lambda job: lowered in job.description.lower(), reverse=True)

