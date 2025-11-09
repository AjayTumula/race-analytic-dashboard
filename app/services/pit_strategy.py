import numpy as np
from app.services.data_loader import load_csv_by_pattern

def get_pit_windows(track: str, race: str):
    lap_data, lap_path = load_csv_by_pattern(track, race, "*lap_time*.csv")

    print(f"🔍 Loaded file from: {lap_path}")
    print(f"📊 Columns in lap data: {lap_data.columns.tolist()}")

    # Rename columns to a more standard format
    lap_data = lap_data.rename(columns={
        "value": "LAP_TIME",
        "lap": "LAP_NUMBER",
        "vehicle_id": "NUMBER"
    })

    # Convert time string to seconds
    lap_data["LAP_TIME_SEC"] = lap_data["LAP_TIME"].apply(parse_lap_time)

    pit_windows = {}
    for car_number, group in lap_data.groupby("NUMBER"):
        if group["LAP_TIME_SEC"].isnull().all():
            continue

        median_lap_time = group["LAP_TIME_SEC"].median()
        threshold = median_lap_time * 1.3  # 30% slower is likely a pit stop

        pit_laps = group[group["LAP_TIME_SEC"] > threshold]["LAP_NUMBER"].tolist()
        if pit_laps:
            pit_windows[car_number] = pit_laps

    return pit_windows or {"message": "No pit stops detected via lap-time analysis"}


def parse_lap_time(lap_time_value):
    try:
        # Lap time comes in seconds directly
        return float(lap_time_value) / 1000 if float(lap_time_value) > 1000 else float(lap_time_value)
    except:
        return np.nan
