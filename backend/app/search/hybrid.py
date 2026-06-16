from app.db.models import JobPosting


def hybrid_rank(jobs: list[JobPosting], query: str) -> list[JobPosting]:
    lowered = query.lower()
    terms = lowered.split()
    return sorted(jobs, key=lambda job: _score(job, terms), reverse=True)


def _score(job: JobPosting, terms: list[str]) -> int:
    haystack = f"{job.title} {job.company} {job.description}".lower()
    return sum(term in haystack for term in terms)
