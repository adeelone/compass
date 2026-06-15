# Privacy

- The user owns profile, resumes, generated versions, and job history.
- `.env` holds local secrets and must not be committed.
- Uploaded files should be encrypted at rest with `APP_ENCRYPTION_KEY`.
- OAuth-based imports must require explicit user consent.
- Account deletion must remove resumes, profile data, application history, generated documents, cached embeddings, and uploaded files.
- Recommendations must expose their rule or model source.

