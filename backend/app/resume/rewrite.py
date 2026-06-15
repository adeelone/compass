def rewrite_bullet(bullet: str) -> list[dict[str, str]]:
    base = bullet.rstrip(".")
    return [
        {"angle": "impact", "text": f"Improved {base} by clarifying scope, measurable result, and user or business value."},
        {"angle": "technical depth", "text": f"Engineered {base} using explicit systems, tools, scale, and reliability constraints."},
        {"angle": "leadership", "text": f"Led work to {base.lower()}, aligning stakeholders and documenting repeatable execution."},
    ]

