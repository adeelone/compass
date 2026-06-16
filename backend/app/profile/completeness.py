from app.db.models import CareerProfile


def completeness(profile: CareerProfile) -> tuple[int, list[str]]:
    checks = {
        "Add a headline.": bool(profile.headline),
        "Add at least one experience.": bool(profile.experiences),
        "Add at least five skills.": len(profile.skills) >= 5,
        "Set job preferences.": bool(profile.preferences),
    }
    done = sum(checks.values())
    return round(done / len(checks) * 100), [label for label, passed in checks.items() if not passed]


def public_profile(profile: CareerProfile) -> dict[str, object]:
    allowed = {
        field
        for field, visibility in profile.visibility.items()
        if getattr(visibility, "value", visibility) == "public"
    }
    payload: dict[str, object] = {"name": profile.contact.name}
    if "headline" in allowed and profile.headline:
        payload["headline"] = profile.headline
    if "skills" in allowed:
        payload["skills"] = [skill.name for skill in profile.skills]
    if "projects" in allowed:
        payload["projects"] = [project.model_dump(mode="json") for project in profile.projects]
    return payload
