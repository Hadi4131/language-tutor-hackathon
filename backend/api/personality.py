from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database.repositories import UserRepository
from database.models import PersonalityProfile

router = APIRouter()


async def get_current_user_id():
    """Get current user ID - creates demo user if doesn't exist"""
    user_id = "demo_user_123"
    
    # Check if user exists, create if not
    from database.models import UserModel
    user = await UserRepository.get_user_by_firebase_uid(user_id)
    if not user:
        # Create demo user
        demo_user = UserModel(
            firebase_uid=user_id,
            email="demo@languagetutor.com",
            display_name="Demo User",
            level="intermediate",
        )
        await UserRepository.create_user(demo_user)
    
    return user_id


# Pre-defined AI tutor personalities
PERSONALITIES = {
    "friendly": PersonalityProfile(
        id="friendly",
        name="Friendly Companion",
        description="A warm, encouraging friend who makes learning enjoyable",
        teaching_style="casual",
        sample_response="That's a great effort! Let's work on making it even better together.",
        avatar_emoji="😊",
        system_prompt_modifier="You are a warm, encouraging tutor who celebrates progress and makes learning fun."
    ),
    "strict": PersonalityProfile(
        id="strict",
        name="British Professor",
        description="A precise academic who values accuracy and proper grammar",
        teaching_style="formal",
        sample_response="I must insist on proper grammar. Let us correct this properly.",
        avatar_emoji="👨‍🏫",
        system_prompt_modifier="You are a precise British professor who values accuracy and proper grammar above all."
    ),
    "casual": PersonalityProfile(
        id="casual",
        name="California Friend",
        description="A laid-back buddy who keeps practice chill and conversational",
        teaching_style="casual",
        sample_response="Hey, no worries! Let's just chat and practice naturally.",
        avatar_emoji="🤙",
        system_prompt_modifier="You're a laid-back California friend helping them practice. Keep it chill and conversational."
    ),
    "patient": PersonalityProfile(
        id="patient",
        name="Patient Teacher",
        description="An extremely patient educator who explains everything simply",
        teaching_style="formal",
        sample_response="Take your time. Let me explain this step by step...",
        avatar_emoji="🧘",
        system_prompt_modifier="You are an extremely patient teacher who never rushes and always explains in simple terms."
    ),
    "motivational": PersonalityProfile(
        id="motivational",
        name="Motivational Coach",
        description="An energetic coach who inspires you to push your limits",
        teaching_style="casual",
        sample_response="You've got this! Let's crush this challenge together!",
        avatar_emoji="🔥",
        system_prompt_modifier="You are an energetic coach who motivates and inspires learners to push themselves."
    )
}


class PersonalitySelection(BaseModel):
    personality_id: str


@router.get("/personality/available")
async def get_available_personalities():
    """
    Get list of all available AI tutor personalities
    """
    return {
        "personalities": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "teaching_style": p.teaching_style,
                "sample_response": p.sample_response,
                "avatar_emoji": p.avatar_emoji
            } for p in PERSONALITIES.values()
        ]
    }


@router.get("/personality/{personality_id}")
async def get_personality(personality_id: str):
    """
    Get details of a specific personality
    """
    personality = PERSONALITIES.get(personality_id)
    if not personality:
        raise HTTPException(status_code=404, detail="Personality not found")
    
    return {
        "id": personality.id,
        "name": personality.name,
        "description": personality.description,
        "teaching_style": personality.teaching_style,
        "sample_response": personality.sample_response,
        "avatar_emoji": personality.avatar_emoji
    }


@router.post("/personality/select")
async def select_personality(
    selection: PersonalitySelection,
    user_id: str = Depends(get_current_user_id)
):
    """
    Set user's preferred AI tutor personality
    """
    if selection.personality_id not in PERSONALITIES:
        raise HTTPException(status_code=400, detail="Invalid personality ID")
    
    # Update user's preferred personality
    success = await UserRepository.update_user(
        user_id,
        {"preferred_personality": selection.personality_id}
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update personality")
    
    return {
        "message": "Personality updated successfully",
        "personality": selection.personality_id
    }
