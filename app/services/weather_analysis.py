import numpy as np
from app.services.data_loader import load_csv_by_pattern

def get_weather_data(track: str, race: str):
    df, file_path = load_csv_by_pattern(track, race, "*Weather*Race*.CSV")

    if df.empty:
        return {"message": "No weather data available"}

    print(f"📊 Weather Columns: {df.columns.tolist()}")

    # Summarize weather metrics
    summary = {
        "avg_air_temp": round(df["AIR_TEMP"].mean(), 2),
        "max_track_temp": round(df["TRACK_TEMP"].max(), 2),
        "avg_humidity": round(df["HUMIDITY"].mean(), 2),
        "avg_wind_speed": round(df["WIND_SPEED"].mean(), 2),
        "rain_detected": bool(df["RAIN"].max() > 0),
        "weather_timeline": df[["TIME_UTC_STR", "AIR_TEMP", "TRACK_TEMP", "HUMIDITY", "WIND_SPEED", "RAIN"]].to_dict(orient="records")
    }

    return summary
