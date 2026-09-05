"""Central configuration for RakshaSetu backend.

External integrations are optional. The prototype works with synthetic data
and OpenStreetMap tiles without map credentials.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "RakshaSetu API"
    ENV: str = "development"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    DATABASE_URL: str | None = None
    OPENWEATHER_API_KEY: str | None = None

    # AI provider: openai, google, or anthropic.
    AI_PROVIDER: str = "openai"
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GOOGLE_API_KEY: str | None = None
    GOOGLE_MODEL: str = "gemini-2.5-flash"
    ANTHROPIC_API_KEY: str | None = None
    ANTHROPIC_MODEL: str = "claude-sonnet-4-6"

    MAPBOX_TOKEN: str | None = None
    SMS_API_KEY: str | None = None
    SMS_API_SECRET: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
