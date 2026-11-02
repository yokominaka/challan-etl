# Traffic E-Challan Pipeline & Strategic Analytics (2018–2026)

End-to-End ETL Data Engineering & Machine Learning Analytics Platform for Pakistani Traffic E-Challan Data across major metropolitan districts and provincial jurisdictions (Punjab, Sindh, KPK).

---

## 🌟 Executive Web Dashboard
The project includes a production-grade, executive presentation dashboard at [`index.html`](index.html), built with Tailwind CSS, AOS, and embedded ground-truth analytics.

- **10,000 Verified Records**: Interactive Data Explorer with instant multi-column search, city/vehicle/status filtering, and pagination.
- **Publication Figures**: Dual-pane display of all 6 EDA figures paired with calculated statistics tables:
  1. **City Revenue & Recovery**: Volume vs collection rate across 6 metropolitan centers.
  2. **Enforcement Efficiency**: Verification of payment parity across Automated Cameras (71.2%), Police Officers (69.5%), and Speed Guns (69.4%).
  3. **Weekly Operational Rhythm**: Polar intensity map tracking the Wednesday peak (1,504 citations).
  4. **Strategic Policy Matrix**: Vehicle-specific violation clustering heatmaps.
  5. **Provincial Settlement**: Stacked recovery valuation across Punjab, Sindh, and KPK.
  6. **Fine Distribution & Longitudinal Trends**: Ticket sizing distributions and multi-year collection growth (2018–2026).

---

## 🏗️ Architecture & Tech Stack

```
[FastAPI REST Mock] ➔ [Requests Pagination] ➔ [Pydantic v2 Invariants] ➔ [SQLite ACID Storage] ➔ [Pandas & Seaborn EDA]
```

- **API Layer**: `FastAPI` (streaming paginated JSON batches with realistic network delay)
- **Validation**: `Pydantic v2` (enforcing strict domain business invariants: e.g., zero helmet fines for 4-wheelers, zero seatbelt fines for 2-wheelers, and PKR 0 collected for unpaid citations)
- **Database**: `SQLite` (`echallan_db.sqlite`)
- **Analytics & Visuals**: `Pandas`, `NumPy`, `Seaborn`, `Matplotlib`
- **Dashboard UI**: HTML5, Tailwind CSS, AOS, Vanilla JS

---

## 🚀 Local Quickstart

### 1. View the Dashboard
Simply open `index.html` in any web browser, or run a local HTTP server:
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000`.

### 2. Run the ETL Pipeline
```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI Mock Server (Terminal 1)
uvicorn e_challan_etl.api.main:app --reload --port 8000

# Run Pipeline Execution (Terminal 2)
python e_challan_etl/main.py

# Run Exploratory Data Analysis (EDA)
python e_challan_etl/scripts/eda.py
```

---

## 🌐 Deployment
- **Dashboard (Vercel / GitHub Pages)**: Serves `index.html` directly as a zero-config static site.
- **API (Render / Railway)**: Deployable as a Python Web Service using `uvicorn e_challan_etl.api.main:app --host 0.0.0.0 --port $PORT`.
