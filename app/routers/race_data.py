from fastapi import APIRouter, HTTPException, Query
from app.services.data_loader import list_tracks, list_races
from app.services.race_summary import get_race_summary
from app.services.driver_analysis import analyze_driver_performance
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
