from fastapi import APIRouter, HTTPException
from app.services.race_summary import get_race_summary

router = APIRouter(prefix="/api/races", tags=["Race Data"])

@router.get("/{track}/{race}/summary")
def summary(track: str, race: str):
    """
    Get a summary of the selected race.
    """
    try:
        return get_race_summary(track, race)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
