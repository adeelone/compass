from dataclasses import dataclass
from app.db.models import Resume


@dataclass(frozen=True)
class RuleResult:
    id: str
    label: str
    passed: bool
    severity: str
    fix: str
    source: str


def evaluate_ats(resume: Resume, filename: str = "resume.pdf") -> tuple[int, list[RuleResult]]:
    rules = [
        RuleResult("contact-email", "Contact email parses cleanly", resume.contact.email is not None, "high", "Add one professional email address.", "deterministic:email-regex"),
        RuleResult("standard-sections", "Uses recognizable sections", bool(resume.experience or resume.education or resume.skills), "medium", "Use headings like Experience, Education, and Skills.", "deterministic:section-detection"),
        RuleResult("formatting-spacing", "Avoids table-like spacing", not resume.formatting_warnings, "medium", "Replace table or column layout with simple section flow.", "deterministic:spacing-heuristic"),
        RuleResult("filename", "Filename is recruiter friendly", "resume" in filename.lower() and len(filename) <= 80, "low", "Use a short filename such as FirstLast-Resume.pdf.", "deterministic:filename"),
    ]
    score = round(sum(25 for rule in rules if rule.passed))
    return score, rules

