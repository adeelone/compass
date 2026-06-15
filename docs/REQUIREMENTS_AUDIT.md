# Requirements Audit

Source: `codex_humanize_compass.docx.md` requirements source and supplied test case.

## Summary

- PASS: 13
- PARTIAL: 17
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
| PDF/DOCX/TXT/OCR upload support | PARTIAL | Upload accepts files, but the parser currently decodes text bytes and does not run real PDF/DOCX/OCR extraction. |
| ATS readability scoring | PASS | `backend/app/resume/ats_rules.py` returns deterministic rule results and a 0-100 score. |
| Content quality scoring | PASS | `backend/app/resume/content_scorer.py` scores metrics and action verbs. |
| Canonical profile model | PASS | `CareerProfile` is defined in `backend/app/db/models.py`. |
| Aggregated job feed | PARTIAL | `GET /api/jobs` returns scored jobs from the provider registry, currently using the mock provider. |
| Pluggable `JobProvider` | PASS | `JobProvider` and `ProviderMetadata` are defined under `backend/app/jobs/providers`. |
| Greenhouse/Lever/Ashby/Adzuna/USAJobs/Remotive providers | PARTIAL | These sources are documented in `PROVIDERS.md`; only the mock provider is implemented. |
| Hybrid FTS and vector search | PARTIAL | `search_jobs` and `hybrid_rank` exist, but there is no Postgres FTS or vector index yet. |
| Per-job 0-100 match score | PASS | `score_job` returns a bounded score and sourced reasons. |
| Sourced rationale | PASS | Match reasons include `source` and evidence strings. |
| Matched and missing keywords | PASS | `/api/jobs` and `/api/match` return both arrays. |
| Gap-closer resources | PASS | `recommend_resources` returns cited URLs for known missing keywords. |
| Tailored resume export | PARTIAL | `tailored_summary` exists; full versioned resume export is not implemented. |
| Cover letter export | PARTIAL | Tailoring scaffolding exists, but no cover-letter endpoint/export exists. |
| Application tracker and kanban | PARTIAL | Status model and frontend kanban exist; persistence and full workflow are not implemented. |
| Email ingest and reminders | PARTIAL | Feature flags and worker placeholder exist; no email parser or reminder scheduler is implemented. |
| Notifications | PARTIAL | Digest builder exists; in-app/email/push delivery is not implemented. |
| Per-field privacy | PARTIAL | Profile visibility fields exist; enforcement is not implemented. |
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
