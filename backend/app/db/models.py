from datetime import UTC, date, datetime
from enum import Enum
from pydantic import BaseModel, Field


class Visibility(str, Enum):
    private = "private"
    internal = "internal"
    public = "public"


class Contact(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    links: list[str] = Field(default_factory=list)


class Experience(BaseModel):
    company: str
    title: str
    start: date | None = None
    end: date | None = None
    bullets: list[str] = Field(default_factory=list)
    tech_tags: list[str] = Field(default_factory=list)


class Education(BaseModel):
    institution: str
    degree: str | None = None
    field: str | None = None
    graduation: date | None = None


class Skill(BaseModel):
    name: str
    category: str = "general"
    level: int = Field(default=3, ge=1, le=5)
    last_used: date | None = None
    evidence: str | None = None


class Project(BaseModel):
    title: str
    description: str
    tech: list[str] = Field(default_factory=list)
    links: list[str] = Field(default_factory=list)


class Resume(BaseModel):
    contact: Contact
    summary: str | None = None
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    source_text: str = ""
    formatting_warnings: list[str] = Field(default_factory=list)
    parsed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CareerProfile(BaseModel):
    contact: Contact
    headline: str | None = None
    summary_short: str | None = None
    summary_long: str | None = None
    experiences: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    preferences: dict[str, str | int | bool | list[str]] = Field(default_factory=dict)
    visibility: dict[str, Visibility] = Field(default_factory=dict)


class JobSourceKind(str, Enum):
    official_api = "official-api"
    partner_api = "partner-api"
    public_feed = "public-feed"
    best_effort_page = "best-effort-page"


class JobPosting(BaseModel):
    id: str
    title: str
    company: str
    locations: list[str] = Field(default_factory=list)
    is_remote: bool = False
    employment_type: str = "full-time"
    seniority: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str = "USD"
    posted_at: datetime | None = None
    expires_at: datetime | None = None
    description: str
    apply_url: str
    source: str
    source_kind: JobSourceKind
    raw_hash: str
