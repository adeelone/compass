from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Compass"
    environment: str = Field(default="development", alias="ENVIRONMENT")
    database_url: str = Field(default="sqlite:///./compass.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    app_encryption_key: str = Field(default="dev-only-change-me", alias="APP_ENCRYPTION_KEY")
    enable_llm_features: bool = Field(default=False, alias="ENABLE_LLM_FEATURES")
    enable_email_ingest: bool = Field(default=False, alias="ENABLE_EMAIL_INGEST")
    enable_headless_workers: bool = Field(default=False, alias="ENABLE_HEADLESS_WORKERS")
    enable_public_profiles: bool = Field(default=False, alias="ENABLE_PUBLIC_PROFILES")
    enable_push: bool = Field(default=False, alias="ENABLE_PUSH")
    llm_provider: str = Field(default="mock", alias="LLM_PROVIDER")
    embedding_provider: str = Field(default="mock", alias="EMBEDDING_PROVIDER")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

