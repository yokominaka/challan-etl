from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI(
    title="Pakistan E-Challan Data Provider API",
    description="Mock API serving traffic e-challan records for ETL extraction.",
    version="1.0.0",
)

DATA_PATH = "data/punjab_echallans.csv"


@app.get("/")
def health_check():
    return {"status": "online", "endpoint": "/api/v1/challans"}


@app.get("/api/v1/challans")
def get_challans(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Max records to return"
    ),
):
    df = pd.read_csv(DATA_PATH)
    total_records = len(df)

    # Slice data for batch/paginated requests
    paginated_df = df.iloc[skip : skip + limit]

    return {
        "total_records": total_records,
        "skip": skip,
        "limit": limit,
        "data": paginated_df.to_dict(orient="records"),
    }