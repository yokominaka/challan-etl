from scripts.extract import fetch_challan
from scripts.transform import transform_and_validate
from scripts.load import load_to_database

def run_pipeline():
    print("PAKISTAN E CHALLAN ETL")

    raw_records = fetch_challan(batch_size=1000)

    if not raw_records:
        print("no records extracted")
        return

    clean_df = transform_and_validate(raw_records)

    if clean_df.empty:
        print("validation failed!!")
        return

    success = load_to_database(clean_df)

    if success:
        print("PIPLELINE EXECUTED SUCCESSFULLY")

if __name__ == "__main__":
    run_pipeline()