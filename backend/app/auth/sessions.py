from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe


@dataclass(frozen=True)
class Session:
    token: str
    subject: str
    expires_at: datetime


def create_session(subject: str) -> Session:
    return Session(token=token_urlsafe(32), subject=subject, expires_at=datetime.now(UTC) + timedelta(days=7))
