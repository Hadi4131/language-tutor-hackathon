from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from services.speech_service import speech_service
from services.gemini_service import gemini_service
from services.elevenlabs_service import elevenlabs_service
from services.pronunciation_service import pronunciation_service
from middleware.auth_middleware import get_current_user_from_token
from fastapi.responses import JSONResponse
import base64

router = APIRouter()


@router.post("/conversation/audio")
async def process_audio_conversation(
    file: UploadFile = File(...),
    personality: str = "friendly",
    user_level: str = "intermediate",
    user_id: str = None,  # Will be None for unauthenticated, populated by middleware if authenticated
    authorization: str = Header(None)
):
    """
    Simplified: Audio Input -> STT -> Pronunciation -> Gemini -> TTS -> Output
    Supports both authenticated and unauthenticated users
    """
    
    # Try to get authenticated user, fallback to demo if not authenticated
    if authorization:
        try:
            user_id = await get_current_user_from_token(authorization)
        except:
            user_id = "demo_user"
    else:
        user_id = "demo_user"
    
    try:
        # 1. Read Audio
        audio_content = await file.read()
        
        # 2. Transcribe (STT) with word-level confidence scores
        speech_result = await speech_service.transcribe_audio(audio_content)
        transcript = speech_result["transcript"]
        word_confidences = speech_result["word_confidences"]
        
        if not transcript:
             return JSONResponse(status_code=400, content={"message": "Could not recognize audio"})

        # 3. Pronunciation Analysis
        pronunciation_score = pronunciation_service.calculate_pronunciation_score(word_confidences)
        problematic_phonemes = pronunciation_service.identify_problematic_phonemes(word_confidences)
        pronunciation_feedback = pronunciation_service.generate_pronunciation_feedback(
            pronunciation_score, 
            problematic_phonemes
        )
        
        # 4. Analyze with Gemini
        analysis = await gemini_service.analyze_language(
            transcript, 
            user_level=user_level,
            personality=personality
        )
        
        # 5. Generate Response Audio (TTS)
        ai_response_parts = []
        
        if pronunciation_score >= 85:
            ai_response_parts.append("Great pronunciation!")
        elif pronunciation_score < 65:
            ai_response_parts.append(pronunciation_feedback)
        
        ai_response_parts.append(analysis.get("learning_tip", ""))
        ai_response_parts.append(analysis.get("follow_up_question", ""))
        
        ai_response_text = " ".join(filter(None, ai_response_parts))
        
        try:
            audio_bytes = await elevenlabs_service.generate_audio(ai_response_text)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        except Exception as e:
            print(f"TTS Generation failed: {e}")
            audio_base64 = None
        
        # 6. Return response
        return {
            "transcript": transcript,
            "analysis": analysis,
            "pronunciation": {
                "score": pronunciation_score,
                "feedback": pronunciation_feedback,
                "problematic_phonemes": problematic_phonemes,
            },
            "audio_base64": audio_base64,
            "user_id": user_id  # Include for debugging
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error processing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
