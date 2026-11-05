from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

BASE_DIR= Path(__file__).resolve().parent.parent
DB_PATH= BASE_DIR / "data" / "echallan_db.sqlite"

engine=create_engine(f"sqlite:///{DB_PATH}")


def load_to_database(
    df: pd.DataFrame,table_name:str="echallan_records"
) -> bool:
    if df.empty:
        print("No data available to load into the database.")
        return False

    print("Starting Database Ingestion...")

    try:
        # table_name first positional argument and con=engine
        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)

        print(
            f"Successfully loaded {len(df)} records into SQLite table'{table_name}'!"
        )
        print(f"📁 Database file saved at:{DB_PATH}\n")
        return True

    except Exception as e:
        print(f"Error loading data into database:{e}")
        return False


if __name__ == "__main__":
    from extract import fetch_challan
    from transform import transform_and_validate

    raw_data=fetch_challan(batch_size=1000)
    clean_df=transform_and_validate(raw_data)
    load_to_database(clean_df)