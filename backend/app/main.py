from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api import (
    villages,
    hazards,
    risk,
    safesites,
    relocation,
    alerts,
    history,
    reports,
    assistant,
    live,
    routing,
    regions,
)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="RakshaSetu disaster risk and response decision-support API using live and open-data feeds.",
    version="1.0.0",
)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    regions.router,
    villages.router,
    hazards.router,
    risk.router,
    safesites.router,
    relocation.router,
    alerts.router,
    history.router,
    reports.router,
    assistant.router,
    live.router,
    routing.router,
):
    app.include_router(router)


@app.get("/")
def root():
    return {"service": settings.APP_NAME, "status": "ok", "scope": "India", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "healthy", "scope": "India", "mode": "realtime-open-data"}
