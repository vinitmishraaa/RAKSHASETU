"""Central configuration for RakshaSetu backend."""
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings

BACKEND_ENV=Path(__file__).resolve().parents[2]/".env"
ROOT_ENV=Path(__file__).resolve().parents[3]/".env"
class Settings(BaseSettings):
    APP_NAME:str="RakshaSetu API"; ENV:str="development"; CORS_ORIGINS:str="http://localhost:5173,http://127.0.0.1:5173"
    DATABASE_URL:str|None=None; OPENWEATHER_API_KEY:str|None=None; FIRMS_API_KEY:str|None=None
    AI_PROVIDER:str="openai"; OPENAI_API_KEY:str|None=None; OPENAI_MODEL:str="gpt-4o-mini"
    GOOGLE_API_KEY:str|None=None; GOOGLE_MODEL:str="gemini-2.5-flash"; ANTHROPIC_API_KEY:str|None=None; ANTHROPIC_MODEL:str="claude-sonnet-4-6"
    MAPBOX_TOKEN:str|None=None; SMS_API_KEY:str|None=None; SMS_API_SECRET:str|None=None
    class Config:
        env_file=(str(BACKEND_ENV),str(ROOT_ENV)); extra="ignore"
@lru_cache
def get_settings()->Settings:return Settings()
