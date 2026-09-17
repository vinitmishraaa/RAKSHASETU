<div align="center">

# 🛡️ RAKSHASETU

### Live Disaster Risk • Hazard Monitoring • Mapped Relocation Support

<p>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=111827" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/OpenStreetMap-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white" alt="OpenStreetMap" />
  <img src="https://img.shields.io/badge/NASA_GIBS-0B3D91?style=for-the-badge&logo=nasa&logoColor=white" alt="NASA GIBS" />
</p>

<i>A GIS-based disaster-management dashboard built around live public observations and open geospatial data.</i>

</div>

---

## What changed

RakshaSetu now uses a **live-open-data first** architecture for operational map data. Synthetic village, shelter capacity, occupancy and infrastructure quantities are no longer used by the main settlement, shelter, risk-summary or relocation endpoints.

The application follows a strict rule:

> **If a source does not publish a value, RakshaSetu shows “Not available” instead of inventing a number.**

The UI has also been moved to a clean **light operational theme** using white, orange, yellow, green and light-blue accents.

## Live / Open Sources

| Source | RakshaSetu usage |
|---|---|
| **OpenStreetMap + Overpass API** | Real mapped cities, towns, villages and emergency-shelter locations. |
| **Open-Meteo** | Current temperature, precipitation and wind observations for mapped settlements. |
| **USGS Earthquake Feed** | Public all-day earthquake observations used for live map markers and the live indicator. |
| **NASA GIBS / Earthdata** | Real satellite imagery layer in the Leaflet map. |
| **NASA FIRMS** | Near-real-time fire hotspots when a FIRMS API key is configured. |
| **OSRM** | Open road-network routing where the routing service can resolve the selected endpoints. |

ISRO/NRSC also publishes Bhuvan and disaster-management geospatial services, including satellite and disaster layers. RakshaSetu keeps those sources documented separately because availability, access conditions and redistribution rights differ by service.

## Live risk indicator

The dashboard's current settlement indicator is calculated from **current public observations**, not a fabricated village score:

```text
Live Indicator = max(
    current precipitation component,
    current wind component,
    nearest USGS earthquake proximity component
)
```

This is an **application indicator**, not an official government hazard rating or evacuation order. The API returns the model description and observation timestamp with each record.

## Relocation centres

The Relocation Centres page displays only locations actually returned by OpenStreetMap with shelter-related tags (`amenity=shelter` or `emergency=shelter`).

RakshaSetu does **not** infer:

- shelter capacity
- current occupancy
- remaining beds/spaces
- infrastructure quality
- operational availability

Those values are shown as **Not available** unless a verified operational source provides them. Capacity-aware allocation is therefore disabled rather than calculated from assumptions.

Road routing can still be requested between a mapped settlement and a mapped shelter using their actual coordinates.

## Satellite imagery

The map includes a NASA GIBS VIIRS true-colour layer. The requested imagery date is generated from the current date rather than bundled into the repository as a fake/static image.

Satellite imagery is provided for situational awareness; cloud cover, acquisition timing and sensor limitations can affect what is visible.

## Architecture

```text
                 Public / Open Data
                        │
       ┌────────────────┼───────────────────┐
       ▼                ▼                   ▼
 OpenStreetMap      Open-Meteo          USGS / NASA
 Settlements        Weather             Hazards / Fire
       │                │                   │
       └────────────────┼───────────────────┘
                        ▼
                 FastAPI Live Layer
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       Live indicators       Shelter mapping
              │                   │
              └─────────┬─────────┘
                        ▼
                React + Leaflet UI
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Hazards       Satellite    Relocation
       & Risk         Imagery      & Routing
```

## Technology

- React 18 + TypeScript
- Vite
- Leaflet + React-Leaflet
- FastAPI + Python
- HTTPX
- OpenStreetMap / Overpass
- Open-Meteo
- USGS GeoJSON feeds
- NASA GIBS
- NASA FIRMS (optional key)
- OSRM

## Project structure

```text
RAKSHASETU/
├── backend/
│   └── app/
│       ├── api/
│       ├── data/
│       │   ├── live.py          # live open-data adapters
│       │   └── synthetic.py     # retained for legacy/reference only
│       ├── optimization/
│       ├── risk_engine/
│       └── main.py
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── types/
│       ├── index.css
│       └── light-theme.css
├── docker-compose.yml
├── LICENSE
└── README.md
```

## Run locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Default addresses:

```text
Frontend: http://localhost:5173
Backend:  http://127.0.0.1:8000
Docs:     http://127.0.0.1:8000/docs
```

## Data provenance rules

1. Every live observation carries its source where available.
2. Mapped shelter records link back to their OpenStreetMap object.
3. Unknown quantities remain unknown.
4. No population estimate is substituted when a settlement has no published population tag.
5. No shelter capacity or occupancy is inferred from building type, area or name.
6. Application risk indicators are clearly labelled as model outputs and must not be treated as official warnings.
7. Official disaster-management agencies remain the authority for evacuation and emergency decisions.

## Development note

`backend/app/data/synthetic.py` remains in the repository only for legacy/reference compatibility. The main live settlement, shelter, risk-summary and relocation paths no longer use it for operational quantities.

## Access

Repository: `https://github.com/vinitmishraaa/RAKSHASETU`

### 🛡️ RakshaSetu

<i>Monitor • Assess • Locate • Relocate • Respond</i>

**Built by Vinit Mishra**
