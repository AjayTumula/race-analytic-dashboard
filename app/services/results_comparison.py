import pandas as pd
import numpy as np
from app.services.data_loader import load_csv_by_pattern


def compare_results(track: str, race: str):
    provisional_df, _ = load_csv_by_pattern(track, race, "*Provisional*Race*1*.CSV")
    official_df, _ = load_csv_by_pattern(track, race, "*Results by Class*Official*.CSV")

    # Rename columns for clarity
    provisional_df = provisional_df.rename(columns={
        "POSITION": "POS_provisional",
        "VEHICLE": "VEHICLE_provisional"
    })
    official_df = official_df.rename(columns={
        "POS": "POS_official",
        "VEHICLE": "VEHICLE_official"
    })

    print(f"✅ Provisional Columns: {provisional_df.columns.tolist()}")
    print(f"✅ Official Columns: {official_df.columns.tolist()}")

    # Merge both results on the car/driver number
    merged = pd.merge(provisional_df, official_df, on="NUMBER", how="inner", suffixes=("_provisional", "_official"))
    print(f"✅ Merged Columns: {merged.columns.tolist()}")

    if "POS_provisional" not in merged.columns or "POS_official" not in merged.columns:
        raise ValueError(
            "Expected columns 'POS_provisional' and 'POS_official', but found: " + str(merged.columns)
        )

    # Compute the change in position
    merged["position_change"] = merged["POS_provisional"].astype(float) - merged["POS_official"].astype(float)

    # Useful subset to return
    comparison_cols = ["NUMBER", "VEHICLE_provisional", "POS_provisional", "POS_official", "position_change"]

    # Sanitizing NaN and preparing output
    return (
        merged[comparison_cols]
        .replace({pd.NA: None, np.nan: None})
        .sort_values(by="position_change", ascending=False)
        .to_dict(orient="records")
    )
