from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    saved = "saved"
    applied = "applied"
    interviewing = "interviewing"
    offer = "offer"
    closed = "closed"


class Application(BaseModel):
    job_id: str
    status: ApplicationStatus = ApplicationStatus.saved
    notes: list[str] = Field(default_factory=list)
    contacts: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

