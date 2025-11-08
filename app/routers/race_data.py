from fastapi import APIRouter, HTTPException
from app.services.race_summary import get_race_summary
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/races", tags=["Race Data"])

@router.get("/{track}/{race}/summary")
def summary(track: str, race: str):
    """
    Get a summary of the selected race.
    """
    try:
        summary =  get_race_summary(track, race)
        logger.info(f"Race Summary requested: Track={track}, Race={race}, Summary={summary}")
        return summary
    except Exception as e:
        logger.error(f"Error processing summary: {e}")
        raise HTTPException(status_code=400, detail=str(e))
