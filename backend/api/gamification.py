from fastapi import APIRouter, HTTPException, Depends
from database.repositories import (
    AchievementRepository, LeaderboardRepository, 
    UserRepository, ProgressRepository
)
from typing import Optional

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


@router.get("/gamification/stats")
async def get_user_stats(user_id: str = Depends(get_current_user_id)):
    """
    Get comprehensive user statistics including progress, streaks, and achievements
    """
    try:
        user = await UserRepository.get_user_by_firebase_uid(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        progress = await ProgressRepository.get_or_create_progress(user_id)
        achievements = await AchievementRepository.get_user_achievements(user_id)
        rank = await LeaderboardRepository.get_user_rank(user_id)
        
        return {
            "user": {
                "display_name": user.display_name or "Anonymous",
                "level": user.level,
                "total_points": user.total_points,
                "current_streak": user.current_streak,
                "longest_streak": user.longest_streak,
                "rank": rank
            },
            "progress": {
                "total_conversations": progress.total_conversations,
                "overall_pronunciation_score": progress.overall_pronunciation_score,
                "total_practice_time_minutes": progress.total_practice_time_minutes,
                "pronunciation_progress": progress.pronunciation_progress
            },
            "achievements": [
                {
                    "title": ach.title,
                    "description": ach.description,
                    "icon": ach.icon,
                    "earned_at": ach.earned_at.isoformat()
                } for ach in achievements
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gamification/leaderboard")
async def get_leaderboard(
    limit: int = 100,
    country: Optional[str] = None
):
    """
    Get global or filtered leaderboard
    """
    try:
        leaderboard = await LeaderboardRepository.get_global_leaderboard(limit)
        
        # Filter by country if specified
        if country:
            leaderboard = [entry for entry in leaderboard if entry.country == country]
        
        return {
            "leaderboard": [
                {
                    "rank": entry.rank,
                    "display_name": entry.display_name,
                    "total_points": entry.total_points,
                    "current_streak": entry.current_streak
                } for entry in leaderboard
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gamification/achievements/available")
async def get_available_achievements():
    """
    Get list of all available achievements
    """
    from services.gamification_service import GamificationService
    
    service = GamificationService()
    achievements = []
    
    for achievement_type, details in service.ACHIEVEMENTS.items():
        achievements.append({
            "type": achievement_type,
            **details
        })
    
    return {"achievements": achievements}
