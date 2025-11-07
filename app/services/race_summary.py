from app.services.data_loader import load_csv_by_pattern

def get_race_summary(track: str, race: str):
    results = load_csv_by_pattern(track, race, "*Results*Race*Official*.csv")
    laps = load_csv_by_pattern(track, race, "*lap_time*R*.csv")

    summary = {
        "track": track.upper(),
        "race": race,
        "total_drivers": results["DRIVER_NUMBER"].nunique(),
        "total_laps": laps["LAP_NUMBER"].max(),
        "fastest_laps": laps["LAP_TIME"].min(),
        "winner": results.sort_values(by="POS").iloc[0]["DRIVER_NUMBER"]
    }
    return summary