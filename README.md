<div align="center">

# 🛡️ RAKSHASETU

### Disaster Risk • Live Hazard Monitoring • Safe-Site & Relocation Support

<p>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=111827" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="Leaflet" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</p>

<i>A GIS-based disaster-management dashboard for monitoring hazards, assessing risk, finding suitable safe sites and supporting relocation decisions.</i>

<p>
  <a href="https://github.com/vinitmishraaa/RAKSHASETU">💻 GitHub Repository</a>
</p>

</div>

---

## 🚀 About RakshaSetu

**RakshaSetu** is a disaster-management decision-support web application that brings operational information into one dashboard.

It combines **GIS visualisation, risk assessment, live hazard observations, vulnerable-location analysis, safe-site selection, relocation planning, alerts, analytics and AI-assisted information access**.

The current prototype is designed around regional disaster-management workflows and includes demonstration coverage for:

- West Bengal
- Bihar
- Sikkim
- Odisha

The application keeps prototype/synthetic records separate from external live observations where applicable.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗺️ **GIS Command Centre** | Interactive map with monitored locations, hazards and safe sites. |
| ⚠️ **Risk Assessment** | Calculates and classifies risk using hazard, exposure and vulnerability factors. |
| 🌋 **Live Hazard Monitoring** | Displays available public hazard observations such as earthquakes and fire hotspots. |
| 🏘️ **Vulnerable Locations** | Shows population and location-level vulnerability information. |
| 🏠 **Safe-Site Ranking** | Ranks potential shelters using safety, capacity, accessibility, distance and infrastructure factors. |
| 🛣️ **Relocation Planning** | Supports capacity-aware relocation planning and road-network routing when available. |
| 🔔 **Alerts** | Provides severity-based alerts with location context and recommended actions. |
| 📊 **Analytics** | Regional, district and risk-class summaries with population-at-risk information. |
| 🛰️ **Satellite Layer** | Supports NASA GIBS imagery for additional situational awareness. |
| 🤖 **AI Assistant** | Provides answers using the application's available risk and relocation context. |
| 🧭 **Navigation Handoff** | Can hand selected locations to Google Maps using their coordinates. |

---

## 🧩 How It Works

```text
                 🌐 External / Application Data
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       Hazards         Location Data     Risk Data
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  🧠 Risk & Decision Layer
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
      Risk Score      Safe-Site Rank    Relocation Plan
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  🗺️ RakshaSetu Dashboard
                           │
        ┌──────────┬───────┼────────┬──────────┐
        ▼          ▼       ▼        ▼          ▼
     Command     Villages Safe    Alerts   Analytics
     Centre               Sites
                           │
                           ▼
                    🤖 AI Assistant
```

---

## ⚠️ Risk Assessment

RakshaSetu uses an explainable prototype risk model based on three major dimensions:

```text
Risk Score =
    Hazard × 0.40
  + Exposure × 0.30
  + Vulnerability × 0.30
```

Risk categories used by the prototype:

```text
75–100    CRITICAL
50–74.9   HIGH
30–49.9   MODERATE
0–29.9    LOW
```

The dashboard can show the factors contributing to a location's risk so that the score is not treated as a black-box result.

---

## 🏠 Safe-Site & Relocation Planning

The relocation module evaluates available safe sites instead of selecting a location only by distance.

```text
Candidate Safe Sites
        ↓
Safety + Capacity + Accessibility
        ↓
Distance + Facilities + Infrastructure
        ↓
Suitability Ranking
        ↓
Capacity Check
        ↓
Relocation Plan
        ↓
Road Route / Navigation
```

The prototype also supports multi-site allocation when a single location cannot accommodate the complete population.

When available, road-network routing is handled through **OSRM**, while navigation can be handed off to Google Maps using exact coordinates.

---

## 🌐 Live Hazard & GIS Sources

RakshaSetu can work with public external sources for situational awareness:

| Source | Usage |
|---|---|
| **USGS** | Earthquake observations including location, magnitude, depth and time. |
| **NASA FIRMS** | Satellite fire-hotspot observations when configured. |
| **NASA GIBS** | Satellite imagery layer for map-based awareness. |
| **OpenStreetMap** | Base map and geographic context. |
| **OSRM** | Road-network routing when available. |
| **Google News RSS** | Regional disaster-related news context. |

External observations are presented as data signals and are not automatically treated as evacuation orders.

---

## 🤖 AI Assistant

The AI Assistant is connected to RakshaSetu's application context so users can access information related to the dashboard's risk and relocation data.

The backend includes support for external AI providers and a local fallback behaviour when an external provider is not configured.

The assistant is intended to work with the information available to the application rather than inventing operational values.

---

## 🏗️ Architecture

```text
                         ┌─────────────────────────┐
                         │      React + Vite       │
                         │   TypeScript Frontend   │
                         └────────────┬────────────┘
                                      │
                                  REST API
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       FastAPI           │
                         │        Backend          │
                         └────────────┬────────────┘
                                      │
               ┌──────────────────────┼──────────────────────┐
               ▼                      ▼                      ▼
         Risk Engine            GIS / Routing          AI Assistant
               │                      │                      │
               ▼                      ▼                      ▼
        Risk + Exposure       OSM / OSRM / GIBS      AI Provider / Fallback
                                      │
                                      ▼
                              RakshaSetu Dashboard
```

---

## 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + TypeScript |
| Build Tool | Vite |
| Routing | React Router |
| Maps | Leaflet + React-Leaflet |
| Charts | Recharts |
| Backend | Python + FastAPI |
| Server | Uvicorn |
| Validation | Pydantic / Pydantic Settings |
| HTTP | HTTPX |
| Configuration | python-dotenv |
| GIS Data | OpenStreetMap |
| Satellite | NASA GIBS |
| Hazard Data | USGS / NASA FIRMS |
| Routing | OSRM |
| AI | Anthropic / OpenAI / Google Gemini integrations |

---

## 📁 Project Structure

```text
RAKSHASETU/
│
├── backend/
│   ├── app/
│   │   ├── ...                 # FastAPI application modules
│   │   └── data/               # Application / prototype data
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── ...                 # React + TypeScript application
│   │   ├── components/
│   │   └── pages/
│   ├── package.json
│   └── vite.config.*
│
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

# 🚀 Access RakshaSetu

## 🌐 GitHub

Repository:

```text
https://github.com/vinitmishraaa/RAKSHASETU
```

## 💻 Run Locally

### Prerequisites

- Python 3.12+
- Node.js 18+
- npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/vinitmishraaa/RAKSHASETU.git
cd RAKSHASETU
```

### 2. Start the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
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

### 3. Start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite will show the local URL, normally:

```text
http://localhost:5173
```

Open that URL in your browser to access the RakshaSetu dashboard.

---

## ⚙️ Environment Configuration

The backend includes an environment template. The core prototype can run without external API keys by using its local/synthetic data and fallback behaviour.

```powershell
cd backend
Copy-Item .env.example .env
```

Optional integrations can be enabled through the corresponding environment variables, including weather, AI, database and map-related services.

```text
OPENWEATHER_API_KEY
ANTHROPIC_API_KEY
MAPBOX_TOKEN
DATABASE_URL
```

Keep credentials in `.env` and never commit API keys or private credentials to the repository.

---

## 📍 Quick Access

| Component | Local Address |
|---|---|
| 🛡️ RakshaSetu Dashboard | `http://localhost:5173` |
| ⚙️ FastAPI Backend | `http://127.0.0.1:8000` |
| 📚 API Documentation | `http://127.0.0.1:8000/docs` |

The dashboard provides access to the main RakshaSetu modules from the application navigation, including the command centre, monitored locations, safe sites, relocation, alerts, analytics and AI assistance.

---

## 🐳 Docker

RakshaSetu also includes Docker configuration for containerised development.

```bash
docker compose up --build
```

The local Python + Vite workflow can be used without Docker for the current prototype.

---

## 🔐 Data & Prototype Notes

The current application includes synthetic/demo records for parts of the operational dataset, including village, population, shelter and historical information.

External live observations are kept conceptually separate from synthetic application records.

For a production deployment, the data layer can be connected to verified operational datasets and a persistent GIS database such as PostgreSQL + PostGIS.

---

## 🔮 Future Scope

- PostgreSQL + PostGIS based persistent data layer
- More verified live hazard feeds
- Advanced disaster-specific risk models
- Expanded alert and escalation workflows
- Stronger authentication and audit logging
- Production-grade notification infrastructure
- More detailed GIS layers and historical analysis
- Additional regional and district datasets

---

<div align="center">

### 🛡️ RakshaSetu

<i>Monitor • Assess • Locate • Relocate • Respond</i>

<p>
  <a href="https://github.com/vinitmishraaa/RAKSHASETU">💻 GitHub Repository</a>
</p>

**Built by Vinit Mishra**

</div>
