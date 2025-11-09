# app/services/pit_strategy.py
import pandas as pd
from app.services.data_loader import load_csv_by_pattern

def get_pit_windows(track: str, race: str):
    lap_data = load_csv_by_pattern(track, race, "*lap_time*.csv")
    if lap_data.empty:
        raise ValueError(f"No lap time data found for {track}/{race}")

    lap_data['lap_number'] = lap_data['LAP_NUMBER'].astype(int)
    lap_data['pit_stop'] = lap_data['CROSSING_FINISH_LINE_IN_PIT'].fillna(False)

    pit_windows = lap_data[lap_data['pit_stop'] == True].groupby('NUMBER')['lap_number'].agg(list)

    return pit_windows.to_dict()
