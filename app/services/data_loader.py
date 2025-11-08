import os, glob, pandas as pd
# from dotenv import load_dotenv

# load_dotenv()
DATA_DIR = os.getenv("CLEANED_DATA_PATH", "cleaned_data")

def list_tracks() -> list[str]:
    if not os.path.isdir(DATA_DIR):
        return []
    return sorted([d for d in os.listdir(DATA_DIR)
                   if os.path.isdir(os.path.join(DATA_DIR, d))])

def list_races(track: str) -> list[str]:
    base = os.path.join(DATA_DIR, track.upper())
    if not os.path.isdir(base): return []
    return sorted([d for d in os.listdir(base)
                   if os.path.isdir(os.path.join(base, d))])

def load_csv_by_pattern(track: str, race: str, pattern: str):
    folder = os.path.join(DATA_DIR, track.upper(), race)
    pats = [os.path.join(folder, pattern)]
    files = []
    for p in pats:
        files += glob.glob(p)
    if not files:
        raise FileNotFoundError(f"No files for pattern '{pattern}' in {folder}")
    if len(files) > 1:
        # keep deterministic pick but alert in logs
        files = sorted(files)
    path = files[0]
    return pd.read_csv(path), path
