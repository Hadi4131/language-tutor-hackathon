from fastapi import APIRouter, HTTPException
from services.elevenlabs_service import elevenlabs_service

router = APIRouter()

@router.get("/voices")
async def get_available_voices():
    """
    Get list of available voices from ElevenLabs.
    """
    try:
        voices = elevenlabs_service.get_voices()
        return {"voices": voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
