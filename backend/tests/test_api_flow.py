from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_upload_jobs_and_match_flow() -> None:
    fixture = Path(__file__).parent / "fixtures" / "sample_resume.pdf"
    with fixture.open("rb") as handle:
        upload = client.post(
            "/api/resume/upload",
            files={"file": ("sample_resume.pdf", handle, "application/pdf")},
        )
    assert upload.status_code == 200
    upload_body = upload.json()
    assert upload_body["resume_id"]
    assert 0 <= upload_body["ats_score"] <= 100
    assert 0 <= upload_body["content_score"] <= 100
    assert upload_body["parsed_sections"]["work"]
    assert upload_body["parsed_sections"]["education"]
    assert upload_body["parsed_sections"]["skills"]

    jobs = client.get("/api/jobs", params={"query": "python intern"})
    assert jobs.status_code == 200
    results = jobs.json()["results"]
    assert results
    first_job = results[0]
    assert 0 <= first_job["score"] <= 100
    assert isinstance(first_job["matched_keywords"], list)
    assert isinstance(first_job["missing_keywords"], list)
    assert first_job["source_attribution"]

    match = client.post(
        "/api/match",
        json={"resume_id": upload_body["resume_id"], "job_id": first_job["id"]},
    )
    assert match.status_code == 200
    match_body = match.json()
    assert match_body["score"] >= 70
    assert "python" in match_body["matched_keywords"]
    assert any(url.startswith("https://") for urls in match_body["gap_closers"].values() for url in urls)


def test_match_returns_404_for_unknown_ids() -> None:
    response = client.post("/api/match", json={"resume_id": "missing", "job_id": "missing"})
    assert response.status_code == 404
