# app/services/weather_analysis.py
import pandas as pd
from app.services.data_loader import load_csv_by_pattern

def get_weather_data(track: str, race: str):
    df = load_csv_by_pattern(track, race, "*Weather*Race*")
    if df.empty:
        raise ValueError(f"No weather data found for {track}/{race}")
    
    # Normalize column names for frontend usage
    df.columns = df.columns.str.lower().str.strip()
    return df.to_dict(orient="records")
