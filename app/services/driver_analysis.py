import numpy as np
import pandas as pd
from app.services.data_loader import load_csv_by_pattern
from app.services.race_summary import parse_lap_time_to_seconds
from app.utils.json_cleaner import make_json_safe

def analyze_driver_performance(track: str, race: str):
    # Load data
    results, _ = load_csv_by_pattern(track, race, "*Results*Official*.csv")
    best_laps, bl_path = load_csv_by_pattern(track, race, "*Best*Laps*.csv")

    # ✅ Detect driver number column
    driver_key = None
    for cand in ["NUMBER", "DRIVER_NUMBER", "CAR", "NO"]:
        if cand in best_laps.columns:
            driver_key = cand
            break
    if not driver_key:
        raise KeyError(f"No driver number column found in {bl_path}. Columns: {best_laps.columns.tolist()}")

    # ✅ Detect lap time columns (BESTLAP_1...BESTLAP_10)
    lap_cols = [col for col in best_laps.columns if col.startswith("BESTLAP_") and not col.endswith("_LAPNUM")]
    if not lap_cols:
        raise KeyError(f"No BESTLAP_X columns found in {bl_path}. Columns: {best_laps.columns.tolist()}")

    # Convert lap time strings into seconds
    for col in lap_cols:
        best_laps[f"{col}_SEC"] = best_laps[col].apply(parse_lap_time_to_seconds)

    # Gather lap stats from *_SEC columns
    sec_cols = [f"{col}_SEC" for col in lap_cols]
    best_laps["fastest"] = best_laps[sec_cols].min(axis=1)
    best_laps["avg_time"] = best_laps[sec_cols].mean(axis=1)
    best_laps["consistency"] = best_laps[sec_cols].std(axis=1)

    # Clean numeric values
    best_laps = best_laps[[driver_key, "fastest", "avg_time", "consistency"]]

    # Merge driver metadata from results
    results[driver_key] = results["NUMBER"].astype(str)
    best_laps[driver_key] = best_laps[driver_key].astype(str)
    meta_cols = ["NUMBER", "VEHICLE", "POS", "ELAPSED"]
    best_laps = best_laps.merge(results[meta_cols], on=driver_key, how="left")

        # JSON-safe cleanup
    best_laps = best_laps.replace([np.inf, -np.inf], np.nan)
    best_laps = best_laps.where(pd.notnull(best_laps), None)

    # Explicitly cast numeric columns to Python types (fixes NumPy float types)
    for col in ["fastest", "avg_time", "consistency", "POS"]:
        if col in best_laps.columns:
            best_laps[col] = best_laps[col].astype(object)

    print("✅ Cleaned driver performance DataFrame:")
    print(best_laps.head())

    response = {
    "driver_key": driver_key,
    "metrics": best_laps.to_dict(orient="records"),
    "used_file": bl_path,
    }

    return make_json_safe(response)
