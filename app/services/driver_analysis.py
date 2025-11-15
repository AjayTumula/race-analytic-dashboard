import numpy as np
import pandas as pd
from app.services.data_loader import load_csv_by_pattern
from app.services.race_summary import parse_lap_time_to_seconds
from app.utils.json_cleaner import make_json_safe


# -------------------------------------------------------
# 🔧 Normalize inconsistent CSV columns (Race1 vs Race2)
# -------------------------------------------------------
def normalize_columns(df: pd.DataFrame):
    rename_map = {
        "BEST LAP": "BEST_LAP_TIME",
        "BEST LAP TIME": "BEST_LAP_TIME",
        "FASTEST_LAP": "BEST_LAP_TIME",
        "FASTEST_LAP_TIME": "BEST_LAP_TIME",

        "POSITION": "POS",
        "PLACE": "POS",

        "TOTAL_TIME": "ELAPSED",
        "RACE_TIME": "ELAPSED",
        "TIME": "ELAPSED",
    }

    return df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})


def analyze_driver_performance(track: str, race: str):
    # Load required CSV files
    results, _ = load_csv_by_pattern(track, race, "*Results*Official*.csv")
    best_laps, bl_path = load_csv_by_pattern(track, race, "*Best*Laps*.csv")

    # -------------------------------------------------------
    # 🔧 Normalize columns so Race2 matches Race1 schema
    # -------------------------------------------------------
    results = normalize_columns(results)
    best_laps = normalize_columns(best_laps)

    # -------------------------------------------------------
    # 🔍 Detect driver number column
    # -------------------------------------------------------
    driver_key = None
    for cand in ["NUMBER", "DRIVER_NUMBER", "CAR", "NO"]:
        if cand in best_laps.columns:
            driver_key = cand
            break

    if not driver_key:
        raise KeyError(f"No driver number column found in {bl_path}. Found: {best_laps.columns.tolist()}")

    # -------------------------------------------------------
    # 🔍 Detect lap columns BESTLAP_1 ... BESTLAP_X
    # -------------------------------------------------------
    lap_cols = [c for c in best_laps.columns if c.startswith("BESTLAP_") and not c.endswith("_LAPNUM")]

    if not lap_cols:
        raise KeyError(f"No BESTLAP_X columns found in {bl_path}. Found: {best_laps.columns.tolist()}")

    # Convert lap times → seconds
    for col in lap_cols:
        best_laps[f"{col}_SEC"] = best_laps[col].apply(parse_lap_time_to_seconds)

    sec_cols = [f"{col}_SEC" for col in lap_cols]

    # Compute driver metrics
    best_laps["fastest"] = best_laps[sec_cols].min(axis=1)
    best_laps["avg_time"] = best_laps[sec_cols].mean(axis=1)
    best_laps["consistency"] = best_laps[sec_cols].std(axis=1)

    # Reduce to essential columns
    best_laps = best_laps[[driver_key, "fastest", "avg_time", "consistency"]]

    # -------------------------------------------------------
    # 🔄 Merge best laps with results metadata
    # -------------------------------------------------------

    # Ensure driver number in results is string
    if driver_key in results.columns:
        results[driver_key] = results[driver_key].astype(str)
    elif "NUMBER" in results.columns:
        results[driver_key] = results["NUMBER"].astype(str)
    else:
        # Fall back — generate empty column!
        results[driver_key] = None

    best_laps[driver_key] = best_laps[driver_key].astype(str)

    # These may NOT exist in Race2 → safely fallback
    meta_cols = ["NUMBER", "VEHICLE", "POS", "ELAPSED"]

    for col in meta_cols:
        if col not in results.columns:
            print(f"⚠ Missing column in results for Race2: {col}, creating blank fallback.")
            results[col] = None

    best_laps = best_laps.merge(results[meta_cols], on=driver_key, how="left")

    # -------------------------------------------------------
    # 🧹 Cleanup for JSON response
    # -------------------------------------------------------
    best_laps = best_laps.replace([np.inf, -np.inf], np.nan)
    best_laps = best_laps.where(pd.notnull(best_laps), None)

    for col in ["fastest", "avg_time", "consistency", "POS"]:
        if col in best_laps.columns:
            best_laps[col] = best_laps[col].astype(object)

    print("✅ Cleaned driver performance DataFrame:")
    print(best_laps.head())

    return make_json_safe({
        "driver_key": driver_key,
        "metrics": best_laps.to_dict(orient="records"),
        "used_file": bl_path,
    })
