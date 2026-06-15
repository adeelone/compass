# Compass

Compass is an AI-augmented job search, resume intelligence, and career operating system for job seekers who want sourced recommendations, transparent scoring, and one canonical career profile.

![CI](https://img.shields.io/badge/ci-pending-lightgrey)
![License](https://img.shields.io/badge/license-MIT-teal)

## Features

- Resume text intake with deterministic parsing, ATS readability rules, content scoring, best points, weak spots, and rewrite hooks.
- Canonical career profile model for identity, experience, education, projects, skills, preferences, and privacy visibility.
- Job provider abstraction with metadata for source kind, rate limits, cache TTL, supported filters, and ToS notes.
- Transparent per-job matching with sourced score reasons, matched and missing keywords, and learning resources.
- Application pipeline primitives for saved, applied, interviewing, offer, and closed states.
- Next.js dashboard with resume analysis, job feed, profile completeness, and kanban views.

## Assumptions

- This initial scaffold ships a mock provider and deterministic scoring so local development and CI never require live job-board network calls.
- LLM and embedding providers are interfaces behind feature flags. The default provider is `mock`.
- Uploaded files, OCR, OAuth imports, background workers, and production persistence are represented by extension points in this first version.
- The project is created in `compass/` because the requested working directory already contained unrelated projects.

## Quickstart

Docker:

```bash
cp .env.example .env
make dev
```

Bare metal:

```bash
cp .env.example .env
cd backend && python -m pip install -e ".[dev]" && uvicorn app.main:app --reload
cd ../frontend && npm install && npm run dev
```

Open `http://localhost:3000`; the API runs at `http://localhost:8000/api`.

## Test And Quality

```bash
make lint
make typecheck
make test
make eval
```

## Environment

All runtime configuration is declared in `.env.example`. Keep `.env` local and never commit credentials.

## Project Structure

```text
backend/   FastAPI API, scoring, matching, providers, profile, storage
frontend/  Next.js app router UI
infra/     Docker Compose and deploy notes
docs/      Supporting architecture and operations material
```

## Adding A Job Provider

1. Add a provider under `backend/app/jobs/providers/`.
2. Implement `JobProvider.search`.
3. Declare `ProviderMetadata`, including legal posture and rate limits.
4. Register it in `providers/registry.py`.
5. Add a recorded fixture test with synthetic data only.

## Switching AI Providers

Set `ENABLE_LLM_FEATURES=true`, choose `LLM_PROVIDER`, and provide the provider API key. Embeddings follow the same pattern through `EMBEDDING_PROVIDER`. Keep prompts versioned in `PROMPTS.md`.

## Deploy

- Fly.io: create Postgres, Redis, and object storage, then deploy backend and frontend apps separately.
- Railway: provision services from `infra/docker-compose.yml` equivalents and set env vars from `.env.example`.
- VPS: install Docker, copy the repo, create `.env`, and run `docker compose -f infra/docker-compose.yml up -d`.

## Known Limitations And Next Steps

- Browser extension for saving jobs from external sites.
- Recruiter-side view.
- Salary insight confidence intervals.
- Referral graph from consented LinkedIn import.
- Mobile PWA install card.

## Contributing

See `CONTRIBUTING.md`.

## License

MIT.

