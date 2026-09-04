from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api import villages, hazards, risk, safesites, relocation, alerts, history, reports, assistant

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="RakshaSetu - disaster risk, red-zone identification and "
                 "relocation decision-support API.",
    version="0.1.0",
)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(villages.router)
app.include_router(hazards.router)
app.include_router(risk.router)
app.include_router(safesites.router)
app.include_router(relocation.router)
app.include_router(alerts.router)
app.include_router(history.router)
app.include_router(reports.router)
app.include_router(assistant.router)


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}
