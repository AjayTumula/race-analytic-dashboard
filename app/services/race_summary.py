import numpy as np
from app.services.data_loader import load_csv_by_pattern

def parse_lap_time_to_seconds(lap_time_str: str) -> float | None:
    try:
        if not isinstance(lap_time_str, str): return None
        m, s = lap_time_str.strip().split(":")
        return int(m) * 60 + float(s)
    except Exception:
        return None

def get_race_summary(track: str, race: str):
    # Official results (has POS, NUMBER, LAPS, BEST_LAP_TIME, BEST_LAP_KPH)
    results, res_path = load_csv_by_pattern(track, race, "*Results*Official*.csv")

    # JSON-safe primitives
    total_drivers = int(results["NUMBER"].astype(str).nunique())
    total_laps = int(results["LAPS"].max())

    # fastest lap from results
    results["BEST_LAP_SECONDS"] = results["BEST_LAP_TIME"].apply(parse_lap_time_to_seconds)
    idx_min = results["BEST_LAP_SECONDS"].idxmin()
    fastest_lap_formatted = results.loc[idx_min, "BEST_LAP_TIME"]

    # winner by POS
    winner_row = results.sort_values("POS", ascending=True).iloc[0]
    winner_number = str(winner_row["NUMBER"])
    winner_vehicle = winner_row["VEHICLE"] if "VEHICLE" in results.columns else None

    return {
        "track": track.upper(),
        "race": race,
        "files": {"results_official": res_path},
        "metrics": {
            "total_drivers": total_drivers,
            "total_laps": total_laps,
            "fastest_lap": {
                "formatted": fastest_lap_formatted,
                "seconds": float(results.loc[idx_min, "BEST_LAP_SECONDS"]),
                "driver_number": winner_row["NUMBER"] if np.isnan(winner_row["POS"]) else None  # optional
            },
            "winner": {
                "number": winner_number,
                "vehicle": winner_vehicle,
                "pos": int(winner_row["POS"]),
            },
        },
    }
