# EcoLink AI — Smart Municipal Ecosystem Automation Framework

EcoLink AI is a dynamic orchestration framework built to solve structural bottlenecks, manual coordination delays, and lost data intelligence within local municipal response networks. 

Developed under the **SDG 11 (Sustainable Cities and Communities)** framework, this platform replaces slow, manual ticketing workflows with **automated, programmable relationship linkages** that instantly connect Citizens, Local Councils, and Cleanup Crews.

---

## Core Features

### 1. Municipal Command Center (Admin Dashboard)
* **Real-Time Throughput Metrics:** Tracks total processed anomalies, active automated linkages, and AI computation speed live.
* **Programmable Linkages Matrix:** Displays active incidents modeled as real-time nodes. Automatically injects routing logic detailing exactly which municipal crew to deploy, removing manual human triage.

### 2. Citizen Hub (Edge Ingestion Portal)
* **Context-Aware Parsing:** Accepts raw data images and extracts structural categories securely via the Gemini Vision Engine.
* **Metadata Fusion:** Packages hardware GPS coordinates together with form data, converting coordinates into readable localized addresses (e.g., "Bandar Sunway, Selangor").

### 3. AI Eco-Assistant (Contextual Expert System)
* **Direct State Awareness:** The chatbot reads the active database state array live, allowing users to query automated rules or request real-time issue summaries.
* **Native Cross-Lingual Context:** Built-in multi-language processing that seamlessly adapts to localized Malaysian inputs (e.g., Bahasa Melayu, English).

---

## Tech Stack

* **Frontend:** HTML5, Tailwind CSS v4 (Premium UI Layout), Axios Engine.
* **Backend:** FastAPI (Python 3.13), Pydantic Data Validation, Uvicorn ASGI Server.
* **AI Core Engine:** Google GenAI SDK (`gemini-2.5-flash` / `gemini-1.5-flash` vision-matrix architectures).

---

## Project Architecture

```text
├── backend/
│   ├── main.py            # FastAPI application routes & Gemini integration
│   └── requirements.txt   # Backend dependency targets
└── frontend/
    └── index.html         # Single-page web application interface
