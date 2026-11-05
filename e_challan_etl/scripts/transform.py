from datetime import date
from typing import Literal
import pandas as pd
from pydantic import BaseModel, Field, ValidationError, model_validator


# pydantic modal
class EChallanModel(BaseModel):
    Challan_ID: str = Field(..., validation_alias="Challan ID")
    Date: str
    Year: int = Field(..., ge=2018, le=2026)
    Month: str
    Day_of_Week: str
    City: str
    Province: str
    Violation_Type: str
    Vehicle_Type: str
    Enforcement_Method: Literal["Camera","Police Officer","Speed Gun"]
    Fine_Amount_PKR: float = Field(...,ge=0)
    Payment_Status: Literal["Paid","Unpaid","Pending"]
    Amount_Collected_PKR: float = Field(...,ge=0)


    @model_validator(mode="after")
    def verify_payment_consistency(self)->"EChallanModel":

        if (
            self.Payment_Status == "Unpaid"
            and self.Amount_Collected_PKR != 0.0
        ):
            raise ValueError("Unpaid challans cannot have non-zero collection!")
        return self


def transform_and_validate(raw_records: list[dict]) -> pd.DataFrame:
    """Validates records with Pydantic and converts valid items to a Pandas DataFrame."""
    valid_records=[]
    invalid_count=0

    print("Starting Data Validation & Transformation...")

    for record in raw_records:
        try:
            validated_obj = EChallanModel.model_validate(record)
            valid_records.append(validated_obj.model_dump())
        except ValidationError as err:
            invalid_count += 1

            if invalid_count == 1:
                print("Validation Error Details for Record #1:")
                print(err)
                print("\nRaw Record #1 Payload:")
                print(record)
            continue

    print(f"Validated Records: {len(valid_records)}")
    print(f" Invalid Records Dropped: {invalid_count}")

    df = pd.DataFrame(valid_records)

    if not df.empty:

        df["Date"]=pd.to_datetime(df["Date"])

        df["Outstanding_Amount_PKR"] = (
            df["Fine_Amount_PKR"] - df["Amount_Collected_PKR"]
        )
    print("Transformation Complete!\n")
    return df


if __name__ == "__main__":
    from extract import fetch_challan

    raw_data = fetch_challan(batch_size=500)
    df_clean = transform_and_validate(raw_data)

    print("DataFrame Info:")
    print(df_clean.info())
    print("\nSample Validated Rows:")
    print(df_clean.head(10))
