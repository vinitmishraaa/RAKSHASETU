# RakshaSetu

## GIS-Based Disaster Risk, Live Hazard Monitoring & Relocation Decision-Support System

RakshaSetu is a disaster-management command-centre prototype that brings **risk assessment, live hazard observations, vulnerable-location analysis, safe-site selection, relocation routing, alerts, analytics and an AI assistant** into one operational dashboard.

The current demonstration coverage includes:

- West Bengal
- Bihar
- Sikkim
- Odisha

The project combines a **React + TypeScript frontend** with a **FastAPI backend** and integrates GIS/map visualisation, a transparent risk engine, safe-site ranking, road-network routing, live public hazard feeds, regional news context and grounded AI assistance.

> **Prototype data note:** Village, population, shelter inventory, rainfall trends and historical records are synthetic/demo data. Live observations such as earthquakes and FIRMS fire detections are external public-feed observations when configured and available. The application keeps this distinction visible.

---

## Features

### Command Centre
- Region/state-based disaster overview
- Risk distribution and population-at-risk metrics
- Interactive GIS map
- Hazard markers and operational location context
- Centralised view of villages, safe sites and alerts

### Risk Assessment
- Hazard, exposure and vulnerability based scoring
- Risk classification: Critical, High, Moderate and Low
- Explainable risk factors for monitored locations
- Population and vulnerability context

### Live Hazard Monitoring
- USGS earthquake observations
- NASA FIRMS fire hotspots when a FIRMS API key is configured
- NASA GIBS satellite imagery layer
- Exact latitude/longitude retained for map verification
- Human-readable nearby location context for live observations

### Safe-Site & Relocation Planning
- Safe-site suitability ranking
- Capacity-aware shelter selection
- Safety, capacity, accessibility, distance, facilities and infrastructure factors
- Multi-site allocation when one site cannot accommodate the complete population
- OSRM road-network routing when available
- Google Maps navigation hand-off using exact coordinates

### Analytics & Reports
- Overall risk summary
- State/region comparison
- District-level analysis
- Risk-class distribution
- Population-at-risk aggregation
- Generated analytical snapshots from the application dataset

### Alerts & Communication
- Severity-based alert view
- Location, district and state context
- Risk and population information
- Recommended-action workflow
- Email/SMS composition interface
- Browser/test siren behaviour for demonstration

### AI Assistant
- Grounded answers using RakshaSetu application context
- Supports OpenAI, Google Gemini and Anthropic Claude providers
- Avoids inventing supplied numbers, locations, capacities and events
- Local deterministic fallback when an external AI provider is unavailable

---

## Architecture

```text
                    External Public Sources
        ┌─────────────────────────────────────────┐
        │ USGS │ NASA FIRMS │ NASA GIBS           │
        │ OSM  │ OSRM       │ Google News RSS     │
        └──────────────────────┬──────────────────┘
                               │
                               ▼
                 ┌─────────────────────────┐
                 │     FastAPI Backend     │
                 │                         │
                 │ Data → Risk → Optimizer │
                 │ Routing → Alerts → AI   │
                 └────────────┬────────────┘
                              │ REST API
                              ▼
                 ┌─────────────────────────┐
                 │ React + TypeScript UI   │
                 │                         │
                 │ Command Centre          │
                 │ Villages / Safe Sites   │
                 │ Relocation / Alerts     │
                 │ Analytics / AI          │
                 └─────────────────────────┘
```

---

## Technology Stack

**Frontend**
- React 18
- TypeScript
- Vite
- React Router
- Leaflet / React-Leaflet
- Recharts

**Backend**
- Python
- FastAPI
- Uvicorn
- Pydantic / Pydantic Settings
- HTTPX
- Python dotenv configuration

**GIS & External Data**
- OpenStreetMap
- NASA GIBS
- NASA FIRMS
- USGS Earthquake Feed
- OSRM
- Google News RSS
- Google Maps navigation links

**AI**
- OpenAI
- Google Gemini
- Anthropic Claude
- Local grounded fallback

---

## Risk Engine

RakshaSetu uses a transparent prototype risk model:

```text
Risk Score =
    Hazard × 0.40
  + Exposure × 0.30
  + Vulnerability × 0.30
```

Risk classes used by the prototype:

```text
75–100    CRITICAL
50–74.9   HIGH
30–49.9   MODERATE
0–29.9    LOW
```

The model is designed to be explainable and replaceable. These weights and thresholds are prototype parameters and should be calibrated against verified datasets and operational standards before production deployment.

---

## Safe-Site Ranking

The relocation planner evaluates candidate sites instead of selecting only the nearest location.

```text
Safety          30%
Capacity        25%
Accessibility   20%
Distance        10%
Facilities      10%
Infrastructure   5%
```

Available capacity is calculated from the prototype shelter inventory:

```text
Available Capacity = Total Capacity − Current Occupancy
```

The resulting ranking can be used to build a relocation plan that considers both suitability and capacity.

---

## Live Data Sources

### USGS Earthquakes

RakshaSetu can consume the public USGS earthquake GeoJSON feed and display event coordinates, magnitude, depth, timestamp and event information on the map.

### NASA FIRMS

When `FIRMS_API_KEY` is configured, the backend can request satellite fire-hotspot observations for the selected region. The application retains coordinates and observation details such as acquisition time, FRP, confidence and satellite/source information.

A FIRMS hotspot is treated as an observation/signal, not as an automatic evacuation order.

### NASA GIBS

NASA GIBS imagery can be displayed as a near-real-time satellite visualisation layer for situational awareness.

### Regional News

The news module uses Google News RSS for regional disaster-related context. News is used for situational awareness and discovery rather than as an authoritative emergency command source.

---

## Data Model

The current prototype uses an in-memory synthetic data layer so the complete workflow can run without a database.

Monitored village records include fields such as:

- location and administrative information
- population and households
- children, elderly and other vulnerable population
- elevation
- river/road proximity
- embankment condition
- rainfall trend
- flood, cyclone and landslide indicators

Safe-site records include:

- location
- capacity and occupancy
- available capacity
- elevation
- accessibility
- infrastructure
- facilities
- hazard context

The architecture is designed so this data layer can later be replaced with a verified **PostgreSQL + PostGIS** implementation.

---

## Project Structure

```text
RAKSHASETU/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

# Run RakshaSetu Locally

## Prerequisites

Install:

- Python 3.12+
- Node.js 18+
- npm
- Git

External API keys are optional for the core prototype. They are only needed for the corresponding external integrations.

---

## 1. Clone the Repository

```bash
git clone https://github.com/vinitmishraaa/RAKSHASETU.git
cd RAKSHASETU
```

---

## 2. Start the Backend

Open a terminal in the project root:

### Windows PowerShell

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks script execution for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Then start FastAPI:

```powershell
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Start the Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite will provide the local frontend URL, normally:

```text
http://localhost:5173
```

Open that address in a browser to access the RakshaSetu dashboard.

---

## 4. Environment Configuration

Copy the backend example environment file:

```powershell
cd backend
Copy-Item .env.example .env
```

Add only the keys for services you want to enable.

Typical integrations include:

```text
FIRMS_API_KEY
OPENAI_API_KEY
GEMINI_API_KEY
ANTHROPIC_API_KEY
```

The core synthetic-data workflow and local AI fallback can run without all of these keys.

**Do not commit `.env` or API keys to GitHub.**

---

# Quick Access

Once both services are running:

| Component | Address |
|---|---|
| RakshaSetu Dashboard | `http://localhost:5173` |
| FastAPI Backend | `http://127.0.0.1:8000` |
| API Documentation | `http://127.0.0.1:8000/docs` |

The main workflow is available directly from the dashboard through the navigation sections for the command centre, monitored locations, safe sites, relocation, alerts, analytics and AI assistance.

---

# Docker

A Docker Compose configuration is included for containerised deployment and future PostgreSQL/PostGIS integration.

```bash
docker compose up --build
```

The current prototype does not require Docker Compose to run because the backend can use its in-memory synthetic dataset directly.

---

# External Services & Internet Requirement

RakshaSetu has two modes of operation:

**Core prototype mode**
- Synthetic operational dataset
- Local risk calculations
- Safe-site ranking
- Local fallback AI behaviour
- Dashboard and analytics

**Connected mode**
- Live USGS earthquake observations
- NASA FIRMS fire hotspots
- NASA GIBS satellite layer
- OSRM road routing
- Regional news
- External AI providers

Connected features require internet access and, where applicable, valid API credentials.

---

# Prototype Scope

RakshaSetu is currently a **decision-support prototype**. It demonstrates the complete workflow from hazard/context observation to risk analysis, safe-site selection, relocation planning and communication support.

For production deployment, the prototype data layer should be replaced with authoritative operational datasets and the communication, authentication, audit, GIS and infrastructure layers should be hardened for the intended deployment environment.

---

## License

This project is licensed under the terms provided in [`LICENSE`](LICENSE).

---

## Repository

**RakshaSetu — GIS-Based Disaster Risk, Live Hazard Monitoring & Relocation Decision-Support System**

Built as a modular disaster-management prototype combining GIS, risk analytics, live public hazard data, routing, alerts and grounded AI assistance.
