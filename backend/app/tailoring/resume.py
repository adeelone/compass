from app.db.models import CareerProfile, JobPosting


def tailored_summary(profile: CareerProfile, job: JobPosting) -> str:
    skills = ", ".join(skill.name for skill in profile.skills[:5])
    return f"{profile.contact.name} is a {profile.headline or 'candidate'} aligned to {job.title} at {job.company}, with evidence in {skills}."


def render_resume_markdown(profile: CareerProfile, job: JobPosting | None = None) -> str:
    title = f"# {profile.contact.name}"
    if job:
        title += f"\n\nTarget role: {job.title} at {job.company}"
    skills = ", ".join(skill.name for skill in profile.skills)
    experience = "\n".join(
        f"## {item.title}, {item.company}\n" + "\n".join(f"- {bullet}" for bullet in item.bullets)
        for item in profile.experiences
    )
    education = "\n".join(f"- {item.institution} {item.degree or ''}".strip() for item in profile.education)
    return "\n\n".join(part for part in [title, profile.summary_short, f"## Skills\n{skills}", experience, f"## Education\n{education}"] if part)


def cover_letter(profile: CareerProfile, job: JobPosting) -> str:
    return (
        f"Dear {job.company} hiring team,\n\n"
        f"I am interested in the {job.title} role. My background includes "
        f"{', '.join(skill.name for skill in profile.skills[:4])}, and my profile shows direct "
        f"evidence for the work described in your posting.\n\n"
        "Thank you for your consideration.\n"
    )
