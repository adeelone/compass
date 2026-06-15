# Evaluation

`make eval` is reserved for offline checks against labeled synthetic fixtures.

Targets:

- Resume section extraction accuracy at or above 90%.
- ATS rule precision at or above 95% on deterministic fixtures.
- Match explanation shape includes score, reasons, sources, matched keywords, and missing keywords.
- No live provider network calls in CI.

