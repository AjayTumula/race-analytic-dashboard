# app/services/results_comparison.py
import pandas as pd
from app.services.data_loader import load_csv_by_pattern

def compare_results(track: str, race: str):
    official = load_csv_by_pattern(track, race, "*Results*Official*.csv")
    provisional = load_csv_by_pattern(track, race, "*Provisional Results*Race*")

    if official.empty or provisional.empty:
        raise ValueError(f"Could not load both official and provisional results for {track}/{race}")

    merged = provisional.merge(
        official,
        on="NUMBER",
        how="outer",
        suffixes=("_provisional", "_official")
    )

    merged["position_change"] = (
        merged["POS_provisional"].astype(float) - merged["POS_official"].astype(float)
    )

    return merged.to_dict(orient="records")
