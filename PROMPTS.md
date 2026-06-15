# Prompts

LLM features are disabled by default. When enabled, prompts should be versioned here with input schema, output schema, model, and evaluation notes.

## Resume Parser Fallback v1

Input: raw resume text and deterministic parser output.

Expected JSON: structured resume fields plus confidence and citations to source spans.

## Rewrite Assistant v1

Input: original bullet, target role family, evidence from profile.

Expected JSON: three rewrites with angles `impact`, `technical_depth`, and `leadership`.

