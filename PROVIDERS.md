# Providers

| Provider | Kind | Status | Legal posture | Notes |
| --- | --- | --- | --- | --- |
| mock | official-api | shipped | Synthetic test data | CI-safe provider |
| Greenhouse | official-api | planned | Use public board endpoints | Respect company board limits |
| Lever | official-api | planned | Use public postings API | Cache and dedupe |
| Ashby | official-api | planned | Use public job board endpoints | Verify tenant settings |
| USAJobs | public-feed | planned | Requires API key and attribution | User supplies credentials |
| Remotive | public-feed | planned | Public API | Respect documented limits |
| RemoteOK RSS | public-feed | planned | RSS feed | Store source URL |
| Hacker News Who is Hiring | public-feed | planned | Public posts | Parse monthly thread |
| LinkedIn | best-effort-page | blocked by default | User-authenticated browser only | No credential collection |

To add a source, implement `JobProvider`, add metadata, register it, record fixtures, and document ToS notes here.

