from app.db.models import JobPosting


def search_jobs(jobs: list[JobPosting], query: str) -> list[JobPosting]:
    terms = query.lower().split()
    return [
        job
        for job in jobs
        if all(term in f"{job.title} {job.company} {job.description}".lower() for term in terms)
    ]

