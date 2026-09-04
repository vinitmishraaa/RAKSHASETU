# RakshaSetu

GIS-based disaster risk, red-zone identification, and relocation
decision-support prototype for government authorities — built from the
technical approach document (risk engine, safe-site optimizer, alerts,
AI assistant).

This is a **fully working prototype**: React frontend + FastAPI backend,
wired end-to-end, running on a realistic synthetic dataset (6 villages,
4 safe sites, modelled on the low-lying South/North 24 Parganas belt of
West Bengal) so every screen has real numbers to show immediately.
Swap the synthetic data layer for PostGIS + real datasets when you're
ready — the API contracts don't change.

## What's included

- **Frontend** (`frontend/`) — React + TypeScript + Vite, Leaflet map,
  Recharts charts. Pages: Dashboard (map + risk panel + scroll sections),
  Villages, Safe Sites, Relocation, Alerts, Analytics, AI Assistant.
- **Backend** (`backend/`) — FastAPI. Risk engine (hazard / exposure /
  vulnerability / scoring / classification / explainability), relocation
  optimizer (site suitability scoring + capacity-aware allocation),
  alerts engine, AI assistant endpoint.
- **Synthetic data layer** (`backend/app/data/synthetic.py`) — stands in
  for the PostGIS + GIS pipeline until real datasets are connected.
- `docker-compose.yml` for an optional PostGIS + containerized setup.

## Quick start (no Docker, no API keys needed)

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # already done for you — all keys optional/blank
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`. Interactive API docs at
`http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env        # already done for you
npm run dev
```

Frontend runs at `http://localhost:5173`.

Open it — the dashboard, map, villages, safe sites, relocation planner,
alerts, analytics, and AI assistant are all live against the backend.

## API keys — what you actually need

**Nothing is required to run this prototype.** It uses:
- Synthetic hazard/population/safe-site data (no key)
- Free OpenStreetMap map tiles via Leaflet (no key)
- A templated (non-LLM) fallback for the AI Assistant (no key)

Everything below is **optional** and only unlocks a specific real-world
integration. Add whichever you want to `backend/.env` (already created
from `backend/.env.example`):

| Variable | Unlocks | Where to get it |
|---|---|---|
| `ANTHROPIC_API_KEY` | Full natural-language AI Assistant (Claude) instead of the templated fallback | https://console.anthropic.com/ |
| `OPENWEATHER_API_KEY` | Live rainfall/weather ingestion instead of synthetic rainfall trend | https://openweathermap.org/api |
| `MAPBOX_TOKEN` | Swap free OSM tiles for Mapbox vector tiles (nicer styling, needed at production map-traffic scale) | https://www.mapbox.com/ |
| `DATABASE_URL` | Real PostgreSQL + PostGIS instead of in-memory synthetic data | Your own Postgres/PostGIS instance (see `docker-compose.yml`) |
| `SMS_API_KEY` / `SMS_API_SECRET` | Real SMS/WhatsApp alert dispatch (placeholder only — not wired into the UI yet, since government notification channels usually need their own authorized infrastructure) | Your chosen SMS/WhatsApp provider |

**Tell me which of these you actually want turned on** (most people
start with just `ANTHROPIC_API_KEY` for the assistant) and I'll wire up
the corresponding real API calls — right now `ANTHROPIC_API_KEY` is
already coded to work the moment you paste a key in; the others have
clear insertion points marked in the code but use synthetic/fallback
data until you decide to connect them.

## Project structure

```
rakshasetu/
├── frontend/           React + Vite + TypeScript + Leaflet + Recharts
│   └── src/
│       ├── components/ map, risk, villages, relocation, alerts, charts, common
│       ├── pages/       Dashboard, Villages, SafeSites, Relocation, Alerts, Analytics, Assistant
│       ├── services/    api.ts – single place all backend calls go through
│       └── types/       shared TS types matching the backend schemas
├── backend/             FastAPI
│   └── app/
│       ├── api/          one router per resource (villages, hazards, risk, safesites, relocation, alerts, history, reports, assistant)
│       ├── risk_engine/   hazard.py, exposure.py, vulnerability.py, scoring.py, classification.py, explainability.py
│       ├── optimization/  site_scoring.py, capacity.py, relocation.py, routing.py
│       ├── ai_assistant/  assistant.py (Claude-backed, with grounded fallback)
│       ├── data/          synthetic.py (swap for PostGIS later)
│       └── core/          config.py (env var / API key handling)
├── docker-compose.yml    optional PostGIS + containerized backend/frontend
└── README.md
```

## How the risk score is computed

```
risk_score = hazard × 0.4 + exposure × 0.3 + vulnerability × 0.3
```

- **Hazard** — weighted blend of flood/cyclone/landslide hazard values
- **Exposure** — elevation, distance to river/coast, embankment condition
- **Vulnerability** — share of children/elderly/vulnerable population,
  distance to the nearest road (evacuation difficulty)

Classification bands (Critical ≥75, High ≥50, Moderate ≥30, Low <30)
are a starting point only — the source spec is explicit these should be
recalibrated in Phase 2 against real data distribution and field
validation, not treated as final.

## How the relocation recommendation is computed

Each candidate safe site is scored on: Safety 30% · Capacity 25% ·
Accessibility 20% · Distance 10% · Facilities 10% · Infrastructure 5%
(`backend/app/optimization/site_scoring.py`). If the top site can't
absorb the full population, the optimizer automatically produces a
split allocation plan across the next-best sites in ranked order.

## Moving from prototype to production

1. Replace `backend/app/data/synthetic.py` calls with real PostGIS
   queries (villages, hazards, safe sites, history) once verified
   government/OSM/satellite datasets are available.
2. Replace the straight-line `routing.py` with a real road-network
   routing engine (OSRM/GraphHopper) for accurate relocation routes.
3. Recalibrate the risk classification thresholds against real data.
4. Add authentication for authority users (not included in this
   prototype).
5. Connect a real SMS/WhatsApp/voice-siren provider for the Alert &
   Escalation Engine.

## License

MIT — see `LICENSE`.
