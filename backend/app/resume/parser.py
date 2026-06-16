import re
from email.utils import parseaddr
from app.db.models import Contact, Education, Experience, Resume, Skill

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
    experience = _parse_experience(lines)
    education = _parse_education(lines)
    warnings = []
    if "\t" in text or re.search(r" {6,}", text):
        warnings.append("Possible multi-column or table-like spacing detected.")
    return Resume(
        contact=Contact(name=name, email=email),
        experience=experience,
        education=education,
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
    inferred = []
    text = " ".join(lines).lower()
    for name in ["Python", "FastAPI", "PostgreSQL", "React", "Docker", "Redis", "SQL"]:
        if name.lower() in text:
            inferred.append(Skill(name=name, category="technical"))
    if inferred:
        return inferred
    return []


def _parse_experience(lines: list[str]) -> list[Experience]:
    bullets = [line.lstrip("-* ") for line in lines if line.startswith(("-", "*"))]
    if not bullets:
        return []
    company = _line_after(lines, "company") or "Unknown"
    title = _line_after(lines, "title") or "Experience"
    return [Experience(company=company, title=title, bullets=bullets)]


def _parse_education(lines: list[str]) -> list[Education]:
    for index, line in enumerate(lines):
        if line.lower().rstrip(":") in SECTION_ALIASES["education"]:
            institution = lines[index + 1] if index + 1 < len(lines) else "Unknown institution"
            degree = lines[index + 2] if index + 2 < len(lines) else None
            return [Education(institution=institution, degree=degree)]
    return []


def _line_after(lines: list[str], label: str) -> str | None:
    prefix = f"{label}:"
    for line in lines:
        if line.lower().startswith(prefix):
            return line.split(":", 1)[1].strip()
    return None
