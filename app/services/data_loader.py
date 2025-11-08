import os
import glob
import pandas as pd
# from dotenv import load_dotenv

# load_dotenv()

DATA_DIR = os.getenv("CLEANED_DATA_PATH", "cleaned_data")

def load_csv_by_pattern(track: str, race: str, pattern: str):
    """
    Load a CSV file matching the given pattern under track and race folder.
    Example pattern: "*lap_time*R*.csv" for Race1 or Race2
    """
    folder_path = os.path.join(DATA_DIR, track.upper(), race)
    file_pattern = os.path.join(folder_path, pattern)
    files = glob.glob(file_pattern)
    print(glob.glob(file_pattern))
    


    if not files:
        raise FileNotFoundError(f"No files matching pattern '{pattern}' in {folder_path}")
    if len(files) > 1:
        raise FileExistsError(f"Multiple files found for pattern '{pattern}', please be more specific.")

    return pd.read_csv(files[0])
