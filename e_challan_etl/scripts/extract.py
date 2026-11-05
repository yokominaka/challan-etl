import time 
import requests
API_URL="http://127.0.0.1:8000/api/v1/challans"


def fetch_challan(batch_size: int = 500) -> list[dict]:
    #using pagination extract all challan records from the api
    all_records = []
    skip = 0

    print("Starting Data extraction from API...")

    while True:
        response = requests.get(API_URL, params={"skip":skip, "limit":batch_size}, timeout=10)
        if response.status_code!=200:
            print(f"Error fetching data from API. Status code: {response.status_code}")
            break
        payload = response.json() 
        records = payload.get("data",[])

        if not records:
            break

        all_records.extend(records)
        print(f"Fetched {len(records)} records. Total records fetched: {len(all_records)}")
        skip += batch_size
        time.sleep(0.5) 
    print(f"Data extraction completed. {len(all_records)} records fetched in total.")
    return all_records
 
if __name__=="__main__":
    raw_data = fetch_challan(batch_size=1000)
    print(f"sample record: {raw_data[0] if raw_data else 'No records fetched'}")
    


