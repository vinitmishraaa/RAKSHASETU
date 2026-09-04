"""
Central configuration for RakshaSetu backend.

All external API keys are OPTIONAL. The prototype runs entirely on
synthetic data and free/open map tiles (OpenStreetMap) with no keys
at all. Add keys to backend/.env only if you want to switch on the
corresponding real integration.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "RakshaSetu API"
    ENV: str = "development"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- Database (optional; unset = use in-memory synthetic data) ---
    # If you stand up a real Postgres+PostGIS instance, set this and
    # switch app/data/synthetic.py calls over to real repositories.
    DATABASE_URL: str | None = None

    # --- Weather / Rainfall (optional) ---
    # OpenWeatherMap: https://openweathermap.org/api  (free tier available)
    OPENWEATHER_API_KEY: str | None = None

    # --- AI Assistant (optional) ---
    # Anthropic API key. Without it, /api/assistant falls back to a
    # deterministic templated explanation using the same underlying data.
    ANTHROPIC_API_KEY: str | None = None

    # --- Map tiles (optional, only needed for prettier vector tiles) ---
    # Mapbox: https://www.mapbox.com/  (free monthly allowance)
    MAPBOX_TOKEN: str | None = None

    # --- Notifications (optional, not wired up in the prototype) ---
    SMS_API_KEY: str | None = None
    SMS_API_SECRET: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
