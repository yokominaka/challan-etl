from datetime import datetime, timedelta
import os
from pathlib import Path
import random
import pandas as pd

CITIES = {
    "Lahore": "Punjab",
    "Rawalpindi": "Punjab",
    "Faisalabad": "Punjab",
    "Peshawar": "KPK",
    "Karachi": "Sindh",
    "Hyderabad": "Sindh",
}

ENFORCEMENT_METHODS=["Camera", "Police Officer", "Speed Gun"]

VEHICLE_VIOLATIONS ={
    "Motorcycle": [
        "No Helmet",
        "Speeding",
        "One-Way Violation",
        "Signal Violation",
        "Reckless Driving",
        "Using Mobile While Driving",
    ],
    "Car": [
        "Seatbelt Violation",
        "Speeding",
        "Signal Violation",
        "One-Way Violation",
        "Reckless Driving",
        "Using Mobile While Driving",
    ],
    "Rickshaw": [
        "Overloading",
        "Signal Violation",
        "One-Way Violation",
        "No Driving License",
        "Reckless Driving",
    ],
    "Commercial Truck": [
        "Overloading",
        "Lane Violation",
        "Speeding",
        "Seatbelt Violation",
        "Signal Violation",
    ],
    "Bus": [
        "Overloading",
        "Lane Violation",
        "Speeding",
        "Seatbelt Violation",
        "Signal Violation",
    ],
}

VIOLATION_FINES = {
    "Speeding": 1904,
    "No Helmet": 1229,
    "Mobile Phone Use": 1732,
    "Reckless Driving": 4899,
    "Signal Violation": 1500,
    "Seatbelt Violation": 1000,
    "One-Way Violation": 2000,
    "Overloading": 2500,
    "Lane Violation": 1200,
    "No Driving License": 1500,
}


def generate_records(num_records=10000):
    records = []
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2026, 10, 1)
    total_days = (end_date - start_date).days

    for i in range(num_records):
        challan_id = f"PK-{100000 + i}"
        city = random.choice(list(CITIES.keys()))
        province = CITIES[city]

        vehicle = random.choice(list(VEHICLE_VIOLATIONS.keys()))
        violation = random.choice(VEHICLE_VIOLATIONS[vehicle])

    
        random_days = random.randint(0, total_days)
        record_date = start_date + timedelta(days=random_days)

        enforcement = random.choice(ENFORCEMENT_METHODS)
        fine_amount = VIOLATION_FINES.get(violation, 1000)


        payment_status = random.choices(
            ["Paid", "Unpaid"], weights=[0.7, 0.3]
        )[0]
        amount_collected = fine_amount if payment_status == "Paid" else 0.0

        records.append({
            "Challan ID": challan_id,
            "Date": record_date.strftime("%Y-%m-%d"),
            "Year": record_date.year,
            "Month": record_date.strftime("%B"),
            "Day_of_Week": record_date.strftime("%A"),
            "City": city,
            "Province": province,
            "Violation_Type": violation,
            "Vehicle_Type": vehicle,
            "Enforcement_Method": enforcement,
            "Fine_Amount_PKR": fine_amount,
            "Payment_Status": payment_status,
            "Amount_Collected_PKR": amount_collected,
        })

    # Locate base project directory and save output inside data/ folder
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    os.makedirs(data_dir, exist_ok=True)

    df = pd.DataFrame(records)
    output_path = data_dir / "punjab_echallans.csv"
    df.to_csv(output_path, index=False)
    print(
        f"Successfully generated {len(df)}records and saved to '{output_path}'!"
    )


if __name__ == "__main__":
    generate_records()