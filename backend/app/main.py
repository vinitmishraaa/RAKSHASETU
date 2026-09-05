from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api import villages, hazards, risk, safesites, relocation, alerts, history, reports, assistant, live
from app.data import synthetic
from app.data.regional import build_regional_data

settings=get_settings()
regional_villages,regional_sites=build_regional_data()
synthetic.VILLAGES.extend(regional_villages)
synthetic.SAFE_SITES.extend(regional_sites)
app=FastAPI(title=settings.APP_NAME,description="RakshaSetu disaster risk and response decision-support API.",version="0.3.0")
origins=[o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
for router in (villages.router,hazards.router,risk.router,safesites.router,relocation.router,alerts.router,history.router,reports.router,assistant.router,live.router): app.include_router(router)
@app.get("/")
def root(): return {"service":settings.APP_NAME,"status":"ok","docs":"/docs"}
@app.get("/api/health")
def health(): return {"status":"healthy"}
