import numpy as np
import pandas as pd
from app.services.data_loader import load_csv_by_pattern


# Convert MM:SS.ms → seconds
def parse_lap_time_to_seconds(lap_time_str: str):
    try:
        if not isinstance(lap_time_str, str):
            return None
        m, s = lap_time_str.strip().split(":")
        return int(m) * 60 + float(s)
    except Exception:
        return None


# --------------------------------------------------
# Fix inconsistent CSV columns (Race1 vs Race2)
# --------------------------------------------------
def normalize_columns(df: pd.DataFrame):
    rename_map = {
        "BEST LAP TIME": "BEST_LAP_TIME",
        "BEST LAP": "BEST_LAP_TIME",
        "FASTEST_LAP": "BEST_LAP_TIME",
        "POSITION": "POS",
        "PLACE": "POS",
        "TOTAL_TIME": "ELAPSED",
        "RACE_TIME": "ELAPSED",
        "LAP_COUNT": "LAPS",
        "TOTAL_LAPS": "LAPS",
    }
    return df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})


# Convert NumPy → Python types
def to_python(v):
    if isinstance(v, (np.integer, np.int32, np.int64)):
        return int(v)
    if isinstance(v, (np.floating, np.float32, np.float64)):
        return float(v)
    return v


def get_race_summary(track: str, race: str):
    # -----------------------------
    # Load results file
    # -----------------------------
    results, res_path = load_csv_by_pattern(track, race, "*Results*Official*.csv")

    # Normalize column inconsistencies
    results = normalize_columns(results)

    # -----------------------------
    # Total drivers
    # -----------------------------
    if "NUMBER" in results.columns:
        total_drivers = int(results["NUMBER"].astype(str).nunique())
    else:
        total_drivers = len(results)

    # -----------------------------
    # Total laps
    # -----------------------------
    if "LAPS" in results.columns:
        total_laps = int(to_python(results["LAPS"].max()))
    else:
        print("⚠ LAPS missing — setting total_laps = 0")
        total_laps = 0

    # -----------------------------
    # Fastest lap
    # -----------------------------
    fastest_formatted = None
    fastest_seconds = None
    fastest_driver = None

    if "BEST_LAP_TIME" in results.columns:
        results["BEST_LAP_SECONDS"] = results["BEST_LAP_TIME"].apply(parse_lap_time_to_seconds)

        valid = results["BEST_LAP_SECONDS"].notna()
        if valid.any():
            idx = results.loc[valid]["BEST_LAP_SECONDS"].idxmin()
            fastest_formatted = results.loc[idx, "BEST_LAP_TIME"]
            fastest_seconds = float(results.loc[idx, "BEST_LAP_SECONDS"])
            fastest_driver = str(results.loc[idx, "NUMBER"])
    else:
        print("⚠ BEST_LAP_TIME missing — no fastest lap available.")

    # -----------------------------
    # Winner (by POS)
    # -----------------------------
    winner_number = None
    winner_vehicle = None
    winner_pos = None

    if "POS" in results.columns:
        winner_row = results.sort_values("POS").iloc[0]

        winner_number = str(winner_row["NUMBER"]) if "NUMBER" in winner_row else None
        winner_vehicle = winner_row["VEHICLE"] if "VEHICLE" in results.columns else None
        winner_pos = int(to_python(winner_row["POS"]))
    else:
        print("⚠ POS missing — cannot determine winner.")

    # -----------------------------
    # Final JSON-safe response
    # -----------------------------
    return {
        "track": track.upper(),
        "race": race,
        "files": {
            "results_official": res_path
        },
        "metrics": {
            "total_drivers": int(total_drivers),
            "total_laps": int(total_laps),
            "fastest_lap": {
                "formatted": fastest_formatted,
                "seconds": fastest_seconds,
                "driver_number": fastest_driver
            },
            "winner": {
                "number": winner_number,
                "vehicle": winner_vehicle,
                "pos": winner_pos
            }
        }
    }
