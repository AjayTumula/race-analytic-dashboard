from app.services.data_loader import load_csv_by_pattern

def parse_lap_time_to_seconds(lap_time_str: str) -> float:
    try:
        minutes, seconds = lap_time_str.split(":")
        return int(minutes) * 60 + float(seconds)
    except Exception:
        return None

def get_race_summary(track: str, race: str):
    # Load results and lap times
    results = load_csv_by_pattern(track, race, "*Results*Official*.csv")
    laps = load_csv_by_pattern(track, race, "*lap_time*R*.csv")

    # Convert BEST_LAP_TIME to seconds
    results["BEST_LAP_SECONDS"] = results["BEST_LAP_TIME"].apply(parse_lap_time_to_seconds)
    fastest_lap_formatted = results.loc[results["BEST_LAP_SECONDS"].idxmin(), "BEST_LAP_TIME"]

    summary = {
        "track": track.upper(),
        "race": race,
        "total_drivers": int(results["NUMBER"].nunique()),     # Convert to Python int
        "total_laps": int(results["LAPS"].max()),              # Convert to Python int
        "fastest_lap": fastest_lap_formatted,                  # Already a formatted string
        "winner": int(results.sort_values(by="POS").iloc[0]["NUMBER"])
    }
    return summary


