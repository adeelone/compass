# Architecture

Compass separates profile truth, resume renderings, job ingestion, and match analysis.

## Data Model

`CareerProfile` is canonical. `Resume` is a parsed or rendered artifact with source text and formatting warnings. `JobPosting` is normalized across providers with source attribution and raw hash.

## Ingestion Pipeline

Providers return normalized postings. Dedupe uses company, title, location, and content hash signals. Indexing combines Postgres full-text search and vector similarity; the current scaffold includes deterministic placeholders.

## Scoring Pipeline

Resume scoring is deterministic by default. Job scoring combines skill overlap, location compatibility, role level fit, and explicit evidence from the profile and posting.

## Streaming And Workers

Long operations should stream status events to the UI. Background workers own provider refreshes, embedding updates, OCR, email ingest, digest sends, and reminders.

## Resilience

Every provider declares rate limits and cache TTL. Production provider calls should use token buckets, jittered scheduling, circuit breakers, stale-while-revalidate caches, and partial degradation indicators.

