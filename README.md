<div align="center">

# 🛡️ RAKSHASETU (रक्षासेतु)

### Real-Time Multi-Hazard Risk Intelligence, Open-Data Monitoring & Guided Evacuation Infrastructure

<p>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=111827" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Leaflet-1.9-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="Leaflet" />
  <img src="https://img.shields.io/badge/OpenStreetMap-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white" alt="OpenStreetMap" />
  <img src="https://img.shields.io/badge/NASA_GIBS-0B3D91?style=for-the-badge&logo=nasa&logoColor=white" alt="NASA GIBS" />
</p>

<i>An operational decision-support platform designed for disaster management authorities (NDMA, SDRF, District Magistrates, and field response teams) powered entirely by real-time public data, algorithmic evacuation planning, and official escalation corridors.</i>

</div>

---

## 🌟 Key Highlights & System Capabilities

### 1. Strict Geographic Cascade (`State → District → City`)
- **Pan-India Coverage**: Pre-indexed authoritative administrative directory across all **28 States and 8 Union Territories**.
- **Official District Accuracy**: Zero random or out-of-state districts. Selecting **West Bengal** displays strictly its **23 official districts** (including *South 24 Parganas*, *North 24 Parganas*, *Darjeeling*, *Howrah*, *Hooghly*, *Purba Medinipur*, etc.). Non-local entities (e.g. *Jaipur*, which belongs to Rajasthan) are strictly isolated to their home states.
- **Optional City Search**: City/town selection is completely optional with an integrated text search filter.
- **Immediate State-Level Loading**: Selecting a State immediately loads all monitored villages, safe shelters, live weather signals, and analytics without requiring district or city selection first. Selecting a District refines the view seamlessly.

### 2. Zero-Key Real-Time Open-Source Data Pipelines
RakshaSetu connects out-of-the-box to live public APIs without requiring paid keys or synthetic mock data:

| Pipeline | Source / API | Purpose & Usage |
|---|---|---|
| **Live Weather Observations** | [Open-Meteo API](https://open-meteo.com/) | Real-time precipitation (mm), temperature (°C), and wind speed (km/h) across Indian coordinates for flood and cyclone risk calculation. |
| **Seismic Feeds** | [USGS Earthquakes](https://earthquake.usgs.gov/) | Real-time global & Indian subcontinent earthquake feeds; calculates distance to nearest hypocenter and seismic hazard score. |
| **Official Disaster Alerts** | [NDMA SACHET (CAP)](https://sachet.ndma.gov.in/) | Official Government of India Common Alerting Protocol emergency bulletins and warnings. |
| **Global Disaster Bulletins** | [GDACS RSS](https://www.gdacs.org/) | Global Disaster Alert and Coordination System multi-hazard feeds (cyclones, floods, earthquakes). |
| **Road Network Routing** | [OSRM Project](http://project-osrm.org/) | Real turn-by-turn road network geometry, driving distance, and live travel duration calculation. |
| **Satellite Imagery** | [NASA GIBS](https://www.earthdata.nasa.gov/eosdis/science-system-description/eosdis-components/gibs) | Near-real-time satellite imagery layer (VIIRS true-color) rendered directly on the tactical map. |
| **Disaster News** | [Google News RSS](https://news.google.com/) | Localized real-time disaster reporting and press advisories. |
| **Active Fire Hotspots** | [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) | *(Optional)* Satellite active thermal hotspot detection via MODIS / VIIRS when API key is provided. |

### 3. Dynamic Multi-Hazard Risk Engine
- Mathematical risk score calculation from `0 to 100`:
  $$\text{Risk Score} = (H \times 0.40) + (E \times 0.25) + (V \times 0.20) + (A \times 0.15)$$
  Where $H$ = Live Hazard (Open-Meteo rainfall/wind + USGS seismic), $E$ = Settlement Exposure & Population, $V$ = Structural & Demographic Vulnerability, and $A$ = Road Accessibility / Ingress.
- Categorized dynamically into:
  - <span style="color:#e5484d; font-weight:bold;">CRITICAL</span> (Score 75–100)
  - <span style="color:#f2994a; font-weight:bold;">HIGH</span> (Score 50–74)
  - <span style="color:#f5c94a; font-weight:bold;">MODERATE</span> (Score 25–49)
  - <span style="color:#3fb27f; font-weight:bold;">LOW</span> (Score 0–24)

### 4. Tactical Map & Visual Animations
- **Critical Risk Blowout Buffers**: Monitored settlements in the `CRITICAL` risk tier blink with an expanding radar blowout buffer ring (`risk-zone-blowout-critical`) denoting the high-threat perimeter.
- **Safe Shelter Glow**: Verified emergency shelters pulse with a green protective buffer (`safe-pulse-green`).
- **Interactive Layers**: Toggle between Base Map, High-Contrast Topo, NASA GIBS Satellite Imagery, Hazard Signals, and Road Network Evacuation Corridors.

### 5. 4-Step Guided Relocation & Evacuation Corridor
- **Multi-Criteria Optimization**: Mapped evacuation shelters are ranked algorithmically by distance, verified available capacity, road ingress clearance, and emergency facilities.
- **4-Step Official Protocol**:
  1. **Step 1 - Confirm Hazard Perimeter**: Verify danger location, risk score, and exposed population.
  2. **Step 2 - Designated Safe Shelter**: Review primary shelter capacity allocation and multi-criteria rankings.
  3. **Step 3 - Compute Road Network Route**: Generate turn-by-turn driving directions with driving ETA via OSRM.
  4. **Step 4 - Deploy Field Guidance / Navigation**: Seamless hand-off to **Google Maps Driving Navigation** for field transport drivers.
- **Advisory Transparency**: Clear disclaimers stating RakshaSetu provides algorithmic decision support, leaving full operational discretion to incident commanders.

### 6. Officer Alert Desk & Emergency Escalation
- **Designated Response Officers**:
  1. **Anushko Adhikary** (`anushkoadhikary8918@gmail.com` | `+91 8918552039`)
  2. **Medha Mallick** (`medha.mallick2020@gmail.com` | `+91 9007564988`)
  3. **Ayan Acharya** (`ayanacharya06@gmail.com` | `+91 9433172520`)
  4. **Soumyadeep Palit** (`soumyadeeppalit546@gmail.com` | `+91 8697453997`)
  5. **Prithiwi Barui** (`prithiwibarui@gmail.com` | `+91 9748069930`)
  - **Admin / Dispatch Source**: `mishravinit923@gmail.com`
- **Actionable Dispatch**: Instant **Email** (`mailto:`) and **SMS** (`sms:`) triggers pre-populated with location coordinates, alert severity, and recommended response actions.
- **Siren Audio Test**: Dual-tone emergency siren generator powered by the Web Audio API (`sawtooth` oscillator alternating between 720 Hz and 420 Hz).
- **Data Provenance**: Real-time status indicators confirming live connection health for all open data sources.

### 7. Decision Intelligence & Live Risk Analytics
- Interactive data visualizations built with **Recharts**:
  - Horizontal Bar Chart of top settlements by risk score.
  - Donut / Pie Chart showing population distribution across risk tiers.
  - KPI summary cards (Total Settlements Monitored, Population at Risk, Critical Zones, Active Scope).

---

## 🏛️ System Architecture

```text
                                 REAL-TIME OPEN DATA FEEDS
                                             │
         ┌───────────────────┬───────────────┼───────────────┬──────────────────┐
         ▼                   ▼               ▼               ▼                  ▼
    Open-Meteo             USGS            NDMA            GDACS               OSRM
   (Live Weather)      (Seismology)    SACHET (CAP)     (Disasters)       (Road Routing)
         │                   │               │               │                  │
         └───────────────────┼───────────────┴───────────────┘                  │
                             ▼                                                  │
                 FastAPI Backend Service (:8000)                                │
                 ├── app/data/administrative.py (36 States/UTs)                 │
                 ├── app/data/geo_catalog.py (Authoritative Settlements)        │
                 ├── app/data/live.py (Real-Time Ingestion & Weather)           │
                 ├── app/risk_engine/scoring.py (Multi-Hazard Scoring)          │
                 ├── app/optimization/relocation.py (Capacity Allocation)       │
                 └── app/optimization/routing.py ───────────────────────────────┘
                             │
                             ▼ JSON REST Endpoints
                 React 18 + Vite Frontend (:5173)
                 ├── FilterBar (State → District → City Cascade)
                 ├── RiskMap (Leaflet + Animated Radar Blowout Rings)
                 ├── Guided Relocation (4-Step Corridor + Google Maps)
                 ├── Officer Alert Desk (5 Officers + Siren Audio Test)
                 └── Live Analytics (Recharts KPIs & Distributions)
```

---

## 📁 Repository Structure

```text
RAKSHASETU/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── alerts.py         # Unified NDMA SACHET, GDACS, and risk engine alerts
│   │   │   ├── history.py        # Regional disaster history & rainfall profiles
│   │   │   ├── live.py           # Live hazard feeds & weather observations
│   │   │   ├── regions.py        # State, District, and City administrative queries
│   │   │   ├── relocation.py     # Guided relocation plans & OSRM road routes
│   │   │   ├── reports.py        # Executive response summaries
│   │   │   ├── risk.py           # Risk summaries & breakdown indicators
│   │   │   ├── safesites.py      # Mapped evacuation centres & suitability ranking
│   │   │   └── villages.py       # Settlement queries scoped by State/District/City
│   │   ├── data/
│   │   │   ├── administrative.py # Authoritative catalog of all 36 States/UTs & districts
│   │   │   ├── geo_catalog.py    # Spatial coordinates, settlements & safe shelters
│   │   │   ├── live.py           # Real-time weather batching & caching
│   │   │   ├── open_data.py      # SACHET, GDACS, FIRMS & News ingestors
│   │   │   └── synthetic.py      # Catalog fallback bridge
│   │   ├── optimization/
│   │   │   ├── relocation.py     # Relocation capacity planner
│   │   │   ├── routing.py        # OSRM road network router
│   │   │   └── site_scoring.py   # Multi-criteria shelter ranking
│   │   ├── risk_engine/
│   │   │   ├── explainability.py # Transparent scoring rationale generator
│   │   │   ├── hazard.py         # Weather & seismic hazard calculator
│   │   │   └── scoring.py        # Multi-hazard composite risk algorithm
│   │   └── main.py               # FastAPI entry point & CORS configuration
│   ├── .env.example              # Documented open-source and optional API keys
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── alerts/           # Alert summary components
│   │   │   ├── common/           # FilterBar, RiskBadge, Header, Navigation
│   │   │   ├── map/              # RiskMap Leaflet integration & CSS radar animations
│   │   │   ├── relocation/       # RelocationBox & routing cards
│   │   │   ├── risk/             # HazardBars, RegionDetailsPanel, SelectedAreaPanel
│   │   │   └── villages/         # Settlement cards & population profiles
│   │   ├── pages/
│   │   │   ├── Alerts/           # Officer Alert Desk, siren test & live hazard feeds
│   │   │   ├── Analytics/        # Recharts risk distributions & KPIs
│   │   │   ├── Dashboard/        # Command center map, filter cascade & live panels
│   │   │   ├── Relocation/       # 4-step guided evacuation corridor & road routing
│   │   │   ├── SafeSites/        # Mapped emergency shelters directory
│   │   │   └── Villages/         # Monitored settlements directory
│   │   ├── services/
│   │   │   └── api.ts            # Client API client with scope sanitization
│   │   ├── types/
│   │   │   └── index.ts          # TypeScript interfaces & risk types
│   │   ├── App.tsx               # Route definitions
│   │   └── index.css             # Unified dark glassmorphism design system
│   ├── package.json              # Node dependencies & build scripts
│   └── vite.config.ts            # Vite configuration
└── README.md
```

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- Git

### 1. Clone Repository
```bash
git clone https://github.com/vinitmishraaa/RAKSHASETU.git
cd RAKSHASETU
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Review environment configuration
cp .env.example .env

# Launch FastAPI server
uvicorn app.main:app --reload --port 8000
```
Backend will be live at `http://127.0.0.1:8000`  
Swagger API Docs available at `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Frontend will be live at `http://localhost:5173`

---

## ⚙️ Environment Configuration (`backend/.env`)

RakshaSetu requires **zero paid keys** to run completely with live data. Optional API keys can be supplied in `backend/.env` for extended functionality:

```env
ENV=development
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Optional: NASA FIRMS (Satellite active fire hotspots)
# Get a free key at: https://firms.modaps.eosdis.nasa.gov/api/map_key/
FIRMS_API_KEY=

# Optional: AI Assistant (OpenAI / Gemini / Anthropic)
AI_PROVIDER=openai
OPENAI_API_KEY=

# Optional: Production PostgreSQL + PostGIS connection string
DATABASE_URL=
```

---

## 🛡️ Responsible AI & Disaster Data Ethics
1. **No Hallucinated Hazards**: All hazard scores and bulletins reflect empirical measurements from Open-Meteo, USGS, or official government CAP alerts.
2. **Operational Decision Support**: Algorithmic routes and site allocations are advisory recommendations to assist disaster responders. Ground personnel always maintain overriding discretion.
3. **Transparent Provenance**: Every settlement card, alert item, and shelter clearly labels its source, observation timestamp, and data status.

---

<div align="center">

**RAKSHASETU — Bridging Risk Intelligence with Rapid Response**  
*Built for the Smart India Hackathon & National Disaster Resilience*

Developed by **[Vinit Mishra](https://github.com/vinitmishraaa)** & Team

</div>
