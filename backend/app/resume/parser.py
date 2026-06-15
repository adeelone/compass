import re
from email.utils import parseaddr
from app.db.models import Contact, Experience, Resume, Skill

SECTION_ALIASES = {
    "experience": {"experience", "work experience", "employment"},
    "education": {"education"},
    "skills": {"skills", "technical skills", "technologies"},
    "projects": {"projects"},
}


def parse_resume_text(text: str) -> Resume:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = lines[0] if lines else "Unknown Candidate"
    email = _find_email(text)
    skills = _parse_skills(lines)
    bullets = [line.lstrip("-* ") for line in lines if line.startswith(("-", "*"))]
    experience = [Experience(company="Unknown", title="Experience", bullets=bullets)] if bullets else []
    warnings = []
    if "\t" in text or re.search(r" {6,}", text):
        warnings.append("Possible multi-column or table-like spacing detected.")
    return Resume(
        contact=Contact(name=name, email=email),
        experience=experience,
        skills=skills,
        source_text=text,
        formatting_warnings=warnings,
    )


def _find_email(text: str) -> str | None:
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    if not match:
        return None
    _, addr = parseaddr(match.group(0))
    return addr or None


def _parse_skills(lines: list[str]) -> list[Skill]:
    for index, line in enumerate(lines):
        if line.lower().rstrip(":") in SECTION_ALIASES["skills"]:
            raw = " ".join(lines[index + 1 : index + 4])
            names = [part.strip(" .") for part in re.split(r"[,|/]", raw) if part.strip()]
            return [Skill(name=name, category="technical") for name in names[:20]]
    return []

