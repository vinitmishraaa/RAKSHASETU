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

RakshaSetu now follows a **live/open-data first** architecture. Synthetic village, shelter capacity, occupancy and infrastructure quantities are not used by the main operational settlement, shelter, alert, history and relocation flows.

The rule is simple:

> **If a source does not publish a value, RakshaSetu shows “Not available” instead of inventing a number.**

## Live and open data sources

| Source | Usage |
|---|---|
| **SACHET · NDMA** | Official Government of India CAP/RSS disaster alerts. |
| **GDACS** | Global multi-hazard events: earthquake, flood, cyclone, wildfire, drought and volcano feeds. |
| **OpenStreetMap + Overpass** | Real mapped settlements and shelter-tagged locations. |
| **Open-Meteo** | Current temperature, precipitation and wind observations. |
| **USGS** | Public earthquake GeoJSON feed. |
| **NASA FIRMS** | Near-real-time satellite fire hotspots when a FIRMS key is configured. |
| **NASA GIBS** | Near-real-time satellite imagery layer on the map. |
| **IFI-Impacts · IIT Delhi / Zenodo** | Historical India flood inventory covering 1967–2023. |
| **ReliefWeb API** | Humanitarian reports and disaster-response context; requires a pre-approved appname under the current API rules. |
| **OSRM** | Open road-network routing between actual coordinates. |
| **OSDMA** | Official Odisha shelter source documented as a state-level source; operational capacity/availability is not inferred when a machine-readable value is unavailable. |

The live feeds are fetched by the FastAPI backend rather than hard-coded into the frontend.

## Live hazard layer

The live hazard API combines:

- NDMA SACHET official alerts
- GDACS multi-hazard events
- USGS earthquakes
- NASA FIRMS fire detections when configured
- Current public weather observations for settlement indicators

Provider severity is preserved where available. RakshaSetu does not turn a provider alert into an invented evacuation order.

## Historical disaster layer

The historical flood endpoint reads the open **India Flood Inventory-Impacts (IFI-Impacts)** dataset published on Zenodo. The dataset contains flood events from 1967–2023 and is suitable for computational research. citehttps://zenodo.org/records/16994648

Village-level history is not fabricated when the source does not provide a verified village identifier.

## Relocation and shelters

Shelter locations are mapped from real OpenStreetMap shelter/emergency tags and are linked to their source object.

RakshaSetu does **not** invent:

- capacity
- current occupancy
- available beds/spaces
- infrastructure score
- operational status

For routing, the backend exposes a live OSRM route endpoint using the actual origin and destination coordinates.

## Official alert provenance

SACHET is the National Disaster Alert Portal of the National Disaster Management Authority. Its CAP/RSS system is intended for dissemination of alerts from official agencies. The CAP integration guide also documents ETag-based consumption of CAP XML feeds. citehttps://sachet.ndma.gov.in/CapFeed

GDACS publishes free disaster data through its API, including GeoJSON event feeds for multiple hazard types. citehttps://www.gdacs.org/gdacsapi/swagger/index.html

## Satellite imagery

The map includes a NASA GIBS VIIRS true-colour layer. The requested imagery date is derived from the current date rather than bundled as a fake/static image.

## Application risk indicator

Where a settlement has live weather and USGS context, RakshaSetu computes an **application indicator** from the observations returned by those providers.

It is explicitly **not an official government hazard rating**. The observation timestamp and model description are returned with the settlement record.

## Architecture

```text
                 Public / Open Data
                        │
     ┌──────────────────┼───────────────────────┐
     ▼                  ▼                       ▼
  SACHET             GDACS                  OSM/Overpass
  NDMA               hazards               settlements/shelters
     │                  │                       │
     ├──────────────┬───┴──────────────┬────────┘
     ▼              ▼                  ▼
   USGS          NASA FIRMS        Open-Meteo
 earthquake       fire hotspots      weather
     │              │                  │
     └──────────────┴──────────┬───────┘
                               ▼
                         FastAPI Live Layer
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
        React + Leaflet    IFI History        OSRM Route
             │                 │                 │
             └─────────────────┴─────────────────┘
                               ▼
                        RakshaSetu Dashboard
```

## Technology

- React 18 + TypeScript
- Vite
- Leaflet + React-Leaflet
- FastAPI + Python
- HTTPX
- OpenStreetMap / Overpass
- Open-Meteo
- SACHET / NDMA CAP-RSS
- GDACS API
- USGS GeoJSON
- NASA GIBS
- NASA FIRMS (optional key)
- IFI-Impacts / Zenodo
- ReliefWeb API
- OSRM

## Project structure

```text
RAKSHASETU/
├── backend/
│   └── app/
│       ├── api/
│       │   ├── live.py
│       │   ├── alerts.py
│       │   ├── history.py
│       │   └── routing.py
│       ├── data/
│       │   ├── live.py
│       │   ├── open_data.py
│       │   └── synthetic.py       # legacy/reference only
│       ├── optimization/
│       ├── risk_engine/
│       └── main.py
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── types/
│       └── index.css
└── README.md
```

## Run locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
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

## Data-provenance rules

1. Live records retain their provider/source information where available.
2. Unknown quantities remain unknown.
3. Population is not substituted when no reliable source value exists.
4. Shelter capacity and occupancy are never inferred from a name, building type or area.
5. Historical records are sourced from published datasets rather than hand-written incident lists.
6. Application risk indicators are labelled as model outputs.
7. Official agencies remain the authority for emergency warnings and evacuation decisions.

## Access

Repository: `https://github.com/vinitmishraaa/RAKSHASETU`

### 🛡️ RakshaSetu

<i>Monitor • Assess • Locate • Relocate • Respond</i>

**Built by Vinit Mishra**
