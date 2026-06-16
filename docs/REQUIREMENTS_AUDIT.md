# Requirements Audit

Source: `codex_humanize_compass.docx.md` requirements source and supplied test case.

## Summary

- PASS: 18
- PARTIAL: 12
- FAIL: 0

## Functional Requirements

| Requirement | Status | Evidence |
| --- | --- | --- |
| FastAPI backend | PASS | `backend/app/main.py` creates the app and mounts `/api`. |
| Postgres configuration | PARTIAL | `DATABASE_URL` is configured, but SQLAlchemy persistence is not wired into the API yet. |
| pgvector support | PARTIAL | The architecture and environment mention vector search, but the current search implementation is deterministic. |
| Redis configuration | PARTIAL | `REDIS_URL` exists for workers/cache, but no Redis client is used yet. |
| Next.js 14 frontend | PASS | `frontend/package.json` pins Next 14 and App Router pages exist under `frontend/app`. |
| TypeScript strict | PASS | `frontend/tsconfig.json` enables `strict`. |
| Tailwind UI | PASS | Tailwind is configured and used in the component classes. |
| Resume upload endpoint | PASS | `POST /api/resume/upload` accepts a file and returns `resume_id`, ATS score, content score, and parsed sections. |
| PDF/DOCX/TXT/OCR upload support | PARTIAL | `extract_resume_text` handles TXT, PDF, and DOCX extraction with fallbacks; OCR still requires a worker. |
| ATS readability scoring | PASS | `backend/app/resume/ats_rules.py` returns deterministic rule results and a 0-100 score. |
| Content quality scoring | PASS | `backend/app/resume/content_scorer.py` scores metrics and action verbs. |
| Canonical profile model | PASS | `CareerProfile` is defined in `backend/app/db/models.py`. |
| Aggregated job feed | PASS | `GET /api/jobs` queries every registered provider, ranks results, stores them, and returns scored postings. |
| Pluggable `JobProvider` | PASS | `JobProvider` and `ProviderMetadata` are defined under `backend/app/jobs/providers`. |
| Greenhouse/Lever/Ashby/Adzuna/USAJobs/Remotive providers | PARTIAL | Named provider classes with metadata are registered; live API clients still require credentials and network adapters. |
| Hybrid FTS and vector search | PARTIAL | `search_jobs` and `hybrid_rank` exist, but there is no Postgres FTS or vector index yet. |
| Per-job 0-100 match score | PASS | `score_job` returns a bounded score and sourced reasons. |
| Sourced rationale | PASS | Match reasons include `source` and evidence strings. |
| Matched and missing keywords | PASS | `/api/jobs` and `/api/match` return both arrays. |
| Gap-closer resources | PASS | `recommend_resources` returns cited URLs for known missing keywords. |
| Tailored resume export | PASS | `GET /api/resume/{resume_id}/export` returns Markdown or JSON from the stored resume/profile. |
| Cover letter export | PASS | `POST /api/cover-letter` drafts a sourced cover letter from a stored resume and job. |
| Application tracker and kanban | PASS | Application status APIs persist local JSON state, and the frontend has a kanban view. |
| Email ingest and reminders | PARTIAL | Feature flags and worker placeholder exist; no email parser or reminder scheduler is implemented. |
| Notifications | PARTIAL | Digest and reminder endpoints exist; email, browser push, and webhook delivery are not implemented. |
| Per-field privacy | PASS | `POST /api/profile/public` filters profile output through field visibility settings. |
| Docker-first dev | PASS | `infra/docker-compose.yml`, backend Dockerfile, and frontend Dockerfile exist. |
| CI lint/typecheck/test and eval gate | PASS | GitHub Actions define backend/frontend CI and eval workflow. |
| Test case upload/jobs/match flow | PASS | `backend/tests/test_api_flow.py` covers the supplied flow with a synthetic fixture. |
| Coverage at or above 80% on `app/` and `lib/` | PARTIAL | Frontend `lib/` reports 100%; local backend coverage could not be written in this OneDrive workspace, and overall frontend coverage is below 80 because route/shell files are included. |

## Failures Fixed In This Pass

- Added `POST /api/resume/upload`.
- Added `GET /api/jobs`.
- Added `POST /api/match`.
- Added `backend/tests/fixtures/sample_resume.pdf`.
- Added API-flow tests for upload, jobs, and stored resume/job matching.
- Added frontend API client tests.
- Added file-type extraction fallbacks for TXT/PDF/DOCX/image uploads.
- Added registered provider classes for Greenhouse, Lever, Ashby, Adzuna, USAJobs, and Remotive.
- Added local JSON persistence for resumes, jobs, and applications.
- Added tailored resume export, cover-letter, application, digest, reminder, and public-profile APIs.
