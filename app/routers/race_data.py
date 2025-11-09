from fastapi import APIRouter, HTTPException
from app.services.data_loader import list_tracks, list_races, load_csv_by_pattern
from app.services.race_summary import get_race_summary
from app.services.driver_analysis import analyze_driver_performance
from app.services.weather_analysis import get_weather_data
from app.services.results_comparison import compare_results
from app.services.pit_strategy import get_pit_windows
from app.services.prediction import predict_winner
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/races", tags=["Race Data"])

@router.get("/tracks")
def get_tracks():
    return {"tracks": list_tracks()}

@router.get("/{track}/races")
def get_races(track: str):
    races = list_races(track)
    if not races:
        raise HTTPException(404, f"No races found for track {track}")
    return {"track": track.upper(), "races": races}

@router.get("/{track}/{race}/summary")
def race_summary(track: str, race: str):
    try:
        data = get_race_summary(track, race)
        logger.info(f"[SUMMARY] {track}/{race}")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(400, str(e))

@router.get("/{track}/{race}/drivers/analysis")
def driver_analysis(track: str, race: str):
    try:
        data = analyze_driver_performance(track, race)
        logger.info(f"[DRIVER-ANALYSIS] {track}/{race}")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(400, str(e))

@router.get("/{track}/{race}/weather")
def weather_data(track: str, race: str):
    try:
        data = get_weather_data(track, race)
        logger.info(f"[WEATHER] {track}/{race}")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(400, str(e))

@router.get("/{track}/{race}/results/compare")
def compare_race_results(track: str, race: str):
    try:
        data = compare_results(track, race)
        logger.info(f"[COMPARE-RESULTS] {track}/{race}")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(400, str(e))

@router.get("/{track}/{race}/pit-strategy")
def pit_strategy(track: str, race: str):
    try:
        data = get_pit_windows(track, race)
        logger.info(f"[PIT-STRATEGY] {track}/{race}")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(400, str(e))


