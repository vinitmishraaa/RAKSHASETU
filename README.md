<div align="center">

# 🛡️ RAKSHASETU (रक्षासेतु)
### National Multi-Hazard Red-Zone Decision Support & Relocation Management System
**Government of India · Ministry of Home Affairs (MHA) · National Disaster Response Force (NDRF)**

<p>
  <img src="https://img.shields.io/badge/Platform-National_Disaster_Intelligence-0B2545?style=for-the-badge&logo=shield&logoColor=white" alt="National Platform" />
  <img src="https://img.shields.io/badge/Authority-MHA_%7C_NDRF-1D4ED8?style=for-the-badge&logoColor=white" alt="Authority" />
  <img src="https://img.shields.io/badge/Status-Live_Telemetry_Connected-16A34A?style=for-the-badge&logo=status&logoColor=white" alt="Status" />
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=111827" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Leaflet-1.9-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="Leaflet" />
</p>

</div>

---

## 🏛️ Executive Overview

India’s disaster-prone regions face recurrent multi-hazard disruptions including **flash floods**, **landslides**, **coastal erosion**, and **cloudbursts**. Vulnerable habitations historically remain inside high-threat disaster footprints, leading to avoidable loss of lives and critical infrastructure. 

**RakshaSetu (रक्षासेतु)** transitions disaster risk management from *reactive post-calamity emergency response* to an **intelligent, GIS-enabled proactive decision support platform**. Developed under the operational mandate of the **Ministry of Home Affairs (MHA)** and the **National Disaster Response Force (NDRF)**, RakshaSetu dynamically identifies multi-hazard Red Zones unsuitable for permanent habitation, evaluates safe alternative site carrying capacities, and prioritizes vulnerable habitations across structured relocation horizons.

---

## 🎯 Core Strategic Capabilities

### 1. Dynamic Multi-Hazard Red-Zone Delineation
- Continuously models and integrates 4 primary recurring natural hazards:
  1. **Floods & Riverine Inundation**: Live rainfall accumulations, upstream runoff, and river basin elevation vulnerability.
  2. **Landslides & Slope Failure Scarp**: Slope angles, geological slip vulnerability, and terrain saturation.
  3. **Coastal Erosion & Storm Surge**: Tidal ingress, shoreline retreat rates, and cyclonic wind shear.
  4. **Cloudbursts & Flash Precipitation**: High-altitude sudden precipitation spikes from real-time meteorological observations.
- Habitats exceeding critical thresholds ($\text{Risk} \ge 70/100$) are designated as **DECLARED MULTI-HAZARD RED ZONES** (unsuitable for permanent habitation), visualized with expanding animated radar blowout buffers.

### 2. Evidence-Based 3-Pillar Risk Formulation
Habitation risk scores ($0\text{--}100$) are calculated via a transparent composite formulation strictly grounded in empirical telemetry:

$$\text{Risk Score} = (H \times 0.40) + (V_{\text{pop}} \times 0.35) + (\text{Hist} \times 0.25)$$

- **$H$ (Hazard Intensity - 40%)**: Composite live hazard weighting (Floods 25%, Landslides 25%, Coastal Erosion 15%, Cloudbursts 15%, Live Weather & USGS Seismic Telemetry 20%).
- **$V_{\text{pop}}$ (Population Vulnerability - 35%)**: Combines demographic susceptibility (infants, elderly, kutcha housing) and spatial isolation ($V \times 0.6 + E \times 0.4$).
- **$\text{Hist}$ (Disaster History Recurrence - 25%)**: Historical event recurrence frequency and past calamity decadal impacts.

### 3. 3-Tier Relocation Horizons
Habitations are prioritized into actionable administrative operational windows:
- 🔴 **Immediate (0–48 Hours Evacuation)**: Acute, imminent hazard threat requiring emergency tactical evacuation and immediate corridor activation.
- 🟠 **Short-Term (1–3 Months Pre-Monsoon Preparation)**: High recurrent vulnerability requiring scheduled pre-monsoon relocation and temporary relief campus allocation.
- 🟡 **Medium-Term (6–12 Months Sustainable Resettlement)**: Chronic environmental degradation requiring planned permanent township rehabilitation.

### 4. Alternative Site Carrying Capacity & Absorption Stress Matrix
- Evaluates designated safe alternative sites, cyclone shelters, and relief campuses.
- Prevents post-evacuation overcrowding, resource collapse, and secondary hazard exposure by computing:
  $$\text{Utilization Stress \%} = \frac{\text{Pre-Occupancy} + \text{Incoming Evacuee Demand}}{\text{Total Rated Capacity}} \times 100$$
- Sites categorized into:
  - **SAFE ABSORPTION** ($\text{Stress} \le 70\%$): Sufficient shelter headroom, potable water, medical readiness, and backup power.
  - **MODERATE ABSORPTION** ($70\% < \text{Stress} \le 90\%$): Approaching threshold, activates secondary camp readiness.
  - **CAPACITY CRITICAL** ($\text{Stress} > 90\%$): Triggers multi-site split allocation protocol to divert evacuees to adjacent campuses.

### 5. Proactive Resettlement vs. Emergency Tactical Modes
- **Proactive Resettlement Mode**: Focuses on carrying capacity assessment, slope stability indexes, and long-term pre-monsoon town planning.
- **Emergency Tactical Mode**: Locks into live Open-Meteo precipitation, USGS seismic feeds, 0–48h acute alerts, and OSRM turn-by-turn road route dispatch.

---

## 🌟 Technical Infrastructure & Features

### 1. Authoritative Pan-India Administrative Cascade
- **100% Pan-India Scope**: Pre-indexed directory across all **28 States and 8 Union Territories**.
- **Official District Accuracy**: Zero synthetic or misplaced districts. Selecting **West Bengal** displays strictly its **23 official districts** (*South 24 Parganas*, *Darjeeling*, *Howrah*, *Purba Medinipur*, etc.). Non-local districts are isolated strictly to their home states.
- **Instant State-Level Aggregation**: Selecting a State instantly populates all habitations, safe shelters, live weather observations, and risk analytics without requiring sub-district selection.

### 2. Zero-Key Live Public Telemetry Pipelines
RakshaSetu operates fully out-of-the-box using open, public, verifiable data feeds:

| Pipeline | Source / API | Operational Usage |
|---|---|---|
| **Live Meteorological Telemetry** | [Open-Meteo API](https://open-meteo.com/) | Real-time precipitation (mm), temperature, and wind speed for flood and storm surge modeling. |
| **Seismic Observations** | [USGS Earthquakes](https://earthquake.usgs.gov/) | Global & Indian subcontinent real-time earthquake feeds; calculates distance to nearest hypocenter. |
| **Official Disaster Bulletins** | [NDMA SACHET (CAP)](https://sachet.ndma.gov.in/) | Common Alerting Protocol emergency warnings and bulletins from Government of India authorities. |
| **Global Disaster Telemetry** | [GDACS RSS](https://www.gdacs.org/) | Global Disaster Alert and Coordination System multi-hazard feeds. |
| **Road Network Routing** | [OSRM Project](http://project-osrm.org/) | Real turn-by-turn road network geometry, driving distance, and live duration. |
| **Satellite Imagery** | [NASA GIBS](https://www.earthdata.nasa.gov/eosdis/science-system-description/eosdis-components/gibs) | Near-real-time satellite imagery layer (VIIRS true-color) rendered on the command map. |
| **Disaster News & Advisories** | [Google News RSS](https://news.google.com/) | Localized real-time disaster advisories and press releases. |

### 3. Evacuation Corridors & Road Routing
- Computes genuine turn-by-turn road routes from threatened Red Zones to designated safe shelters via the Open Source Routing Machine (OSRM).
- Generates step-by-step navigation instructions with road names, distances, maneuvers, and driving duration.
- Includes 1-click **Open Google Maps Road Navigation** hand-off for field logistics drivers and NDRF evacuation convoys.

### 4. SDMA Relocation Registry & Official Directives
- **1-Click SDMA CSV Registry Export**: Generates official state disaster management habitation registers containing habitations, risk scores, red-zone statuses, and 3-tier relocation classifications.
- **Printable Relocation Orders**: Formal SDMA evacuation directives with unique reference serial numbers, date-stamps, and designated officer signing blocks.

### 5. Automated Emergency Officer Dispatch & Siren Audio
- Pre-configured emergency escalation desk connecting directly to 5 field coordinators:
  - **Anushko Adhikary** (`anushkoadhikary8918@gmail.com`)
  - **Medha Mallick** (`medha.mallick2020@gmail.com`)
  - **Ayan Acharya** (`ayanacharya06@gmail.com`)
  - **Soumyadeep Palit** (`soumyadeeppalit546@gmail.com`)
  - **Prithiwi Barui** (`prithiwibarui@gmail.com`)
- One-click pre-formatted emergency email and SMS dispatch containing exact GPS coordinates, risk tier, and tactical instructions.
- Web Audio API dual-tone siren tester (`720 Hz / 420 Hz`) for operational readiness drills.

---

## 🏛️ System Architecture

```text
                                  REAL-TIME PUBLIC DATA TELEMETRY
                                                 │
             ┌───────────────────────┬───────────┴───────────┬───────────────────────┐
             ▼                       ▼                       ▼                       ▼
        Open-Meteo                 USGS                    NDMA                    OSRM
       (Live Weather)          (Seismology)            SACHET (CAP)           (Road Routing)
             │                       │                       │                       │
             └───────────────────────┼───────────────────────┘                       │
                                     ▼                                               │
                         FastAPI Backend (:8000)                                     │
                         ├── app/data/administrative.py (All 36 States/UTs)          │
                         ├── app/data/geo_catalog.py (Official Habitations)          │
                         ├── app/data/live.py (Real-Time Ingestion & Weather)        │
                         ├── app/risk_engine/hazard.py (4-Hazard Engine)             │
                         ├── app/risk_engine/scoring.py (0.40H + 0.35V + 0.25Hist)   │
                         ├── app/optimization/relocation.py (Capacity Matrix)        │
                         └── app/optimization/routing.py ────────────────────────────┘
                                     │
                                     ▼ JSON REST Endpoints
                         Vite + React 18 Frontend (:5173)
                         ├── TopRibbon (National Tricolor Bar, Emblem, MHA Branding)
                         ├── FilterBar (State → District → City Administrative Cascade)
                         ├── RiskMap (Leaflet + Radar Blowout Buffers + Satellite)
                         ├── Relocation Desk (4-Step Corridor + Google Maps Hand-off)
                         ├── Safe Sites Directory (Carrying Capacity & Stress Gauge)
                         ├── Officer Alert Desk (5 Liaison Officers + Audio Siren)
                         └── Analytics (Recharts 3-Tier Horizons & 4-Hazard Breakdown)
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
│   │   │   ├── safesites.py      # Mapped evacuation centres & carrying capacity
│   │   │   └── villages.py       # Settlement queries scoped by State/District/City
│   │   ├── data/
│   │   │   ├── administrative.py # Authoritative catalog of all 36 States/UTs & districts
│   │   │   ├── geo_catalog.py    # Spatial coordinates, settlements & safe shelters
│   │   │   ├── live.py           # Real-time weather batching & caching
│   │   │   ├── open_data.py      # SACHET, GDACS, FIRMS & News ingestors
│   │   │   └── synthetic.py      # Catalog fallback bridge
│   │   ├── optimization/
│   │   │   ├── relocation.py     # Carrying capacity & absorption stress planner
│   │   │   ├── routing.py        # OSRM road network router
│   │   │   └── site_scoring.py   # Multi-criteria shelter ranking
│   │   ├── risk_engine/
│   │   │   ├── explainability.py # Transparent scoring rationale generator
│   │   │   ├── hazard.py         # 4-hazard engine (Floods, Landslides, Erosion, Cloudbursts)
│   │   │   └── scoring.py        # 3-pillar risk formulation algorithm
│   │   └── main.py               # FastAPI entry point & CORS configuration
│   ├── .env.example              # Documented configuration parameters
│   └── requirements.txt          # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── alerts/           # Alert summary components
│   │   │   ├── common/           # FilterBar, TopRibbon, Gov Header, Badges
│   │   │   ├── map/              # RiskMap Leaflet integration & CSS radar animations
│   │   │   ├── relocation/       # RelocationBox & routing cards
│   │   │   ├── risk/             # HazardBars, RegionDetailsPanel, SelectedAreaPanel
│   │   │   └── villages/         # Settlement cards & population profiles
│   │   ├── pages/
│   │   │   ├── Alerts/           # Early warning desk, siren drill & officer dispatch
│   │   │   ├── Analytics/        # Disaster analytics, 3-tier horizons & hazard charts
│   │   │   ├── Assistant/        # AI decision desk for operational officers
│   │   │   ├── Dashboard/        # Command center map, filter cascade & live panels
│   │   │   ├── Relocation/       # Guided evacuation corridor & road routing
│   │   │   ├── SafeSites/        # Carrying capacity assessment & alternative sites
│   │   │   └── Villages/         # Field habitations directory & SDMA CSV export
│   │   ├── services/
│   │   │   └── api.ts            # Client API client with scope sanitization
│   │   ├── types/
│   │   │   └── index.ts          # TypeScript interfaces & risk types
│   │   ├── App.tsx               # Route definitions
│   │   ├── index.css             # Base reset & structural layout
│   │   ├── light-theme.css       # Official Government of India design system & palette
│   │   └── module-polish.css     # Clean card and metric polish
│   ├── package.json              # Node dependencies & build scripts
│   └── vite.config.ts            # Vite configuration
├── start_all.bat                 # One-click Windows development launcher
├── docker-compose.yml            # Docker deployment configuration
└── README.md
```

---

## 🚀 Quickstart & Deployment

### Method 1: One-Click Windows Launcher (Recommended)
Double-click `start_all.bat` in the repository root. This automatically:
1. Launches the FastAPI backend service on `http://127.0.0.1:8000`.
2. Starts the Vite React frontend on `http://localhost:5173`.
3. Opens your default web browser to the Command Center.

---

### Method 2: Manual Development Setup

#### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**

#### Step 1: Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
- Backend API: `http://127.0.0.1:8000`
- Interactive OpenAPI Docs: `http://127.0.0.1:8000/docs`

#### Step 2: Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```
- Frontend UI: `http://localhost:5173`

---

## ⚙️ Environment Configuration (`backend/.env`)

RakshaSetu requires **zero paid API keys** to run completely with live data. Optional settings can be supplied in `backend/.env` for extended telemetry:

```env
ENV=development
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Optional: NASA FIRMS (Satellite active fire hotspots)
# Free registration at: https://firms.modaps.eosdis.nasa.gov/api/map_key/
FIRMS_API_KEY=

# Optional: AI Operational Assistant
AI_PROVIDER=openai
OPENAI_API_KEY=

# Optional: Production PostgreSQL + PostGIS database connection
DATABASE_URL=
```

---

## 🛡️ Disaster Governance & Operational Transparency

1. **No Hallucinated Hazard Telemetry**: All risk indicators reflect verifiable observations from Open-Meteo, USGS seismology, or official NDMA CAP warning bulletins.
2. **Algorithmic Decision Support**: RakshaSetu generates evidence-based relocation recommendations and carrying capacity assessments to assist disaster managers; field operational discretion remains with on-ground incident commanders.
3. **Data Provenance**: Every settlement card, early warning alert, and shelter capacity rating clearly displays its telemetry source, observation timestamp, and verification status.

---

<div align="center">

**RAKSHASETU (रक्षासेतु) — National Multi-Hazard Decision Support Platform**  
*Government of India · Ministry of Home Affairs · National Disaster Response Force*

Developed by **[Vinit Mishra](https://github.com/vinitmishraaa)**

</div>
