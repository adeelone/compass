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

