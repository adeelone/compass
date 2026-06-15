from app.resume.ats_rules import evaluate_ats
from app.resume.content_scorer import score_content
from app.resume.parser import parse_resume_text


def test_resume_analysis_scores_contact_and_metrics() -> None:
    resume = parse_resume_text("Ada Example\nada@example.com\nSkills\nPython, React\n- Built API used by 120 teams")
    ats_score, rules = evaluate_ats(resume, "ada-resume.pdf")
    content_score, best, findings = score_content(resume)
    assert ats_score >= 75
    assert all(rule.source for rule in rules)
    assert content_score >= 80
    assert best
    assert findings == []

