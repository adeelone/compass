from app.db.models import CareerProfile, JobPosting


def tailored_summary(profile: CareerProfile, job: JobPosting) -> str:
    skills = ", ".join(skill.name for skill in profile.skills[:5])
    return f"{profile.contact.name} is a {profile.headline or 'candidate'} aligned to {job.title} at {job.company}, with evidence in {skills}."

