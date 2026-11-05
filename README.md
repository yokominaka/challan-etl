# Traffic E-Challan Pipeline & Strategic Analytics (2018-2026)

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-Render-emerald?style=for-the-badge&logo=render)](https://challan-etl.onrender.com/)
[![API Docs](https://img.shields.io/badge/API_Docs-Swagger-0ea5e9?style=for-the-badge&logo=fastapi)](https://challan-etl.onrender.com/docs)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-e92063?style=for-the-badge&logo=pydantic)](https://docs.pydantic.dev/)

An end-to-end data engineering and statistical machine learning analytics platform auditing **10,000 validated citations** (2018-2026) across major metropolitan districts and provincial jurisdictions (Punjab, Sindh, KPK).

---

## 🌐 Live Production Links

- **Executive Web Dashboard:** [https://challan-etl.onrender.com/](https://challan-etl.onrender.com/)
- **Interactive API Documentation:** [https://challan-etl.onrender.com/docs](https://challan-etl.onrender.com/docs)
- **API Health Check:** [https://challan-etl.onrender.com/health](https://challan-etl.onrender.com/health)
- **GitHub Repository:** [https://github.com/yokominaka/challan-etl](https://github.com/yokominaka/challan-etl)

---

## 🌟 Executive Presentation Dashboard

The root web application (`index.html`) is a production-grade, single-page executive analytics portal featuring:
- **Clean White Interface:** Eye-friendly aesthetic with soft slate typography, subtle borders, and smooth emerald accents.
- **10,000 Original Validated Records:** Interactive Data Explorer with live multi-column search, multi-filter dropdowns (City, Vehicle Type, Payment Status), and pagination.
- **Original High-Resolution Figures:** Click-to-zoom Lightbox modal for all 6 generated EDA figures paired with ground-truth statistical summary tables.

---

## 📊 Ground-Truth Analytical Findings (Objectives 1-7)

| Metric | Ground-Truth Value | Description |
| :--- | :--- | :--- |
| **Total Citations Audited** | `10,000` | 100% Pydantic v2 schema-validated |
| **Total Fine Assessed** | `PKR 19,510,934` | Gross assessed citation value |
| **Total Revenue Collected** | `PKR 13,664,692` | Actual realized revenue |
| **Overall Recovery Rate** | `70.04%` | Strict settlement consistency |

### Objective Breakdown:
1. **City Revenue & Recovery (`obj1_city_revenue_recovery.png`):**
   - High recovery rate consistency across all 6 metropolitan districts: **Faisalabad (71.1%)**, **Lahore (70.8%)**, **Hyderabad (70.7%)**, **Peshawar (70.6%)**, **Karachi (68.5%)**, and **Rawalpindi (68.4%)**.
2. **Enforcement Channel Parity (`obj2_enforcement_efficiency.png`):**
   - Verified behavioral equivalence: **Automated Cameras (71.2%)**, **Police Officers (69.5%)**, and **Speed Guns (69.4%)**. Drivers settle automated digital citations with the same compliance as in-person officer stops.
3. **Weekly Operational Rhythm (`obj3_weekly_operational_rhythm.png`):**
   - Polar intensity analysis traces peak operational enforcement volume on **Wednesdays (1,504 citations, PKR 2.07M)**, with consistent enforcement volume throughout the weekend.
4. **Strategic Policy Matrix (`obj4_strategic_policy_matrix.png`):**
   - Vehicle-specific infraction clustering: Buses primarily commit lane infractions (21.6%) and overloading (21.1%); Cars cluster around speeding (18.0%) and mobile phone use (17.2%); Rickshaws exhibit high one-way violations (21.1%).
5. **Provincial Fine Assessment (`obj5_provincial_revenue_breakdown.png`):**
   - Stacked settlement status analysis confirms uniform compliance across provincial administrations: **KPK (70.6%)**, **Punjab (70.1%)**, and **Sindh (69.6%)**.
6. **Fine Sizing & Multi-Year Growth (2018-2026) (`obj6_7_fine_dist_yearly_trends.png`):**
   - Fine ticket amounts cluster around median values of PKR 1,500-2,000. Annual collection grew steadily from **PKR 1.46M in 2018** to **PKR 1.62M in 2025**.

---

## 🏗️ Architecture & Pipeline Walkthrough

```
[FastAPI REST Mock] ➔ [Requests Pagination] ➔ [Pydantic v2 Validation] ➔ [SQLite ACID Storage] ➔ [Pandas & Seaborn EDA]
```

1. **FastAPI Mock API Layer (`e_challan_etl/api/`):**
   - Streams paginated batches with realistic latency, query parameters (`skip`, `limit`), and error handling.
   - Dual-serves the executive dashboard at `/` and OpenAPI Swagger documentation at `/docs`.
2. **Requests Ingestion Engine (`e_challan_etl/scripts/extract.py`):**
   - Robust batch extraction with exponential retry backoff, chunked requests, and cursor pagination.
3. **Pydantic v2 Validation Invariants (`e_challan_etl/scripts/transform.py`):**
   - **Constraint 1:** Zero helmet fines permitted on 4-wheelers (Car, Bus, Truck); strictly restricted to Motorcycles.
   - **Constraint 2:** Zero seatbelt fines permitted on 2-wheelers; strictly restricted to 4-wheelers.
   - **Constraint 3:** Unpaid fines strictly enforce `PKR 0.00` collected revenue (accounting integrity).
4. **SQLite Storage Layer (`e_challan_etl/scripts/load.py`):**
   - Transactional, idempotent storage into relational schema (`echallan_records`) with primary keys and indices.
5. **Analytics & Visualization (`e_challan_etl/scripts/eda.py`):**
   - Aggregations and statistical modeling in Pandas; publication-grade exports in Seaborn and Matplotlib.

---

## 📁 Repository Structure

```
.
├── index.html                           # Executive Web Dashboard (HTML5, Tailwind, AOS)
├── requirements.txt                     # Production dependencies (FastAPI, Uvicorn, Pandas, etc.)
├── README.md                            # Project documentation
├── .gitignore                           # Git ignore rules
├── data/
│   └── punjab_echallans.csv             # Validated dataset (10,000 records)
├── reports/
│   └── figures/                         # High-resolution generated plots (Obj 1 to 7)
│       ├── obj1_city_revenue_recovery.png
│       ├── obj2_enforcement_efficiency.png
│       ├── obj3_weekly_operational_rhythm.png
│       ├── obj4_strategic_policy_matrix.png
│       ├── obj5_provincial_revenue_breakdown.png
│       └── obj6_7_fine_dist_yearly_trends.png
└── e_challan_etl/
    ├── api/
    │   └── main.py                      # FastAPI REST API & Dashboard server
    ├── data/
    │   ├── echallan_db.sqlite           # SQLite relational database
    │   └── punjab_echallans.csv         # Raw CSV records
    ├── notebooks/
    │   └── eda.ipynb                    # Interactive Jupyter notebook
    ├── scripts/
    │   ├── extract.py                   # API extraction with pagination
    │   ├── transform.py                 # Pydantic v2 validation logic
    │   ├── load.py                      # SQLite database loader
    │   ├── eda.py                       # Analytical plotting script
    │   └── generate_data.py             # Synthetic generator with domain constraints
    ├── main.py                          # Pipeline orchestrator
    └── run_project.ps1                  # PowerShell automated runner
```

---

## 🚀 Local Development Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/yokominaka/challan-etl.git
cd challan-etl
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run with the Automated PowerShell Runner (Windows)
```powershell
.\e_challan_etl\run_project.ps1
```

### 4. Or Run Manually Step-by-Step

**Terminal 1 — Start FastAPI Server & Dashboard:**
```bash
uvicorn e_challan_etl.api.main:app --reload --port 8000
```
Open [http://localhost:8000](http://localhost:8000) to view the executive dashboard, or [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

**Terminal 2 — Run ETL Pipeline:**
```bash
python e_challan_etl/main.py
```

**Terminal 3 — Re-generate Visualizations & Analytics:**
```bash
python e_challan_etl/scripts/eda.py
```

---

## ☁️ Deployment

- **Render (Live):** Configured as a Web Service running `uvicorn e_challan_etl.api.main:app --host 0.0.0.0 --port $PORT`. Serves both the interactive dashboard at `/` and the REST endpoints at `/api/v1/challans`.
- **Vercel / GitHub Pages (Optional):** Can also be hosted as a zero-config static site by pointing to `index.html`.
