from app.db.models import JobPosting


def build_digest(jobs: list[JobPosting]) -> str:
    lines = ["# Compass Daily Digest", ""]
    for job in jobs[:10]:
        lines.append(f"- {job.title} at {job.company}: {job.apply_url}")
    return "\n".join(lines)


def reminder_message(job_title: str, days_since_update: int) -> str:
    return f"Follow up on {job_title}; it has been {days_since_update} days since the last update."
