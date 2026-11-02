from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import pandas as pd

app = FastAPI(
    title="Traffic E-Challan Pipeline & Analytics Portal",
    description="Traffic e-challan data provider API and executive presentation dashboard.",
    version="1.0.0",
)

# Robust dynamic path resolution
CURRENT_DIR = Path(__file__).resolve().parent
MODULE_DIR = CURRENT_DIR.parent
ROOT_DIR = MODULE_DIR.parent if (MODULE_DIR.parent / "index.html").exists() else MODULE_DIR

# Find DATA_PATH dynamically
possible_data_paths = [
    ROOT_DIR / "data" / "punjab_echallans.csv",
    MODULE_DIR / "data" / "punjab_echallans.csv",
    Path("data/punjab_echallans.csv"),
    Path("e_challan_etl/data/punjab_echallans.csv"),
]
DATA_PATH = next((p for p in possible_data_paths if p.exists()), possible_data_paths[0])


# Serve executive dashboard HTML directly at root URL "/"
@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    index_candidates = [
        ROOT_DIR / "index.html",
        MODULE_DIR / "index.html",
        Path("index.html"),
    ]
    for idx_path in index_candidates:
        if idx_path.exists():
            return HTMLResponse(content=idx_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Dashboard index.html not found</h1>", status_code=404)


# Dedicated Health Check endpoint
@app.get("/api/v1/health")
@app.get("/health")
def health_check():
    return {
        "status": "online",
        "dashboard": "/",
        "api_docs": "/docs",
        "endpoint": "/api/v1/challans",
    }


# Paginated Challan API Endpoint
@app.get("/api/v1/challans")
def get_challans(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
):
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Dataset CSV not found on server")
    df = pd.read_csv(DATA_PATH)
    total_records = len(df)
    paginated_df = df.iloc[skip : skip + limit]

    return {
        "total_records": total_records,
        "skip": skip,
        "limit": limit,
        "data": paginated_df.to_dict(orient="records"),
    }


# Static asset routes for figures and CSV
@app.get("/reports/figures/{filename}")
@app.get("/e_challan_etl/reports/figures/{filename}")
def serve_figure(filename: str):
    candidates = [
        ROOT_DIR / "reports" / "figures" / filename,
        MODULE_DIR / "reports" / "figures" / filename,
        Path(f"reports/figures/{filename}"),
        Path(f"e_challan_etl/reports/figures/{filename}"),
    ]
    for c in candidates:
        if c.exists():
            return FileResponse(str(c))
    raise HTTPException(status_code=404, detail="Figure not found")


@app.get("/data/{filename}")
@app.get("/e_challan_etl/data/{filename}")
def serve_data_file(filename: str):
    candidates = [
        ROOT_DIR / "data" / filename,
        MODULE_DIR / "data" / filename,
        Path(f"data/{filename}"),
        Path(f"e_challan_etl/data/{filename}"),
    ]
    for c in candidates:
        if c.exists():
            return FileResponse(str(c))
    raise HTTPException(status_code=404, detail="File not found")
