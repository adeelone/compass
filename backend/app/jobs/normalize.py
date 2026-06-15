import hashlib
import re


def normalized_key(company: str, title: str, location: str) -> str:
    raw = "|".join(_clean(part) for part in (company, title, location))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())

