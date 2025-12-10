from datetime import datetime
from typing import Dict, List, Optional
from database.models import AchievementModel, StreakModel
from database.repositories import (
    AchievementRepository, StreakRepository, 
    UserRepository, ProgressRepository
)


class GamificationService:
    """
    Service for managing gamification features including points, achievements, and streaks
    """
    
    # Achievement definitions
    ACHIEVEMENTS = {
        "first_conversation": {
            "title": "First Steps",
            "description": "Completed your first conversation",
            "icon": "🎯",
            "points": 10
        },
        "week_streak": {
            "title": "Week Warrior",
            "description": "Practiced for 7 days in a row",
            "icon": "🔥",
            "points": 50
        },
        "month_streak": {
            "title": "Monthly Master",
            "description": "Practiced for 30 days in a row",
            "icon": "⭐",
            "points": 200
        },
        "pronunciation_master": {
            "title": "Pronunciation Master",
            "description": "Achieved 90+ pronunciation score",
            "icon": "🎤",
            "points": 30
        },
        "error_free": {
            "title": "Perfect Practice",
            "description": "Completed a conversation with no errors",
            "icon": "💎",
            "points": 25
        },
        "ten_conversations": {
            "title": "Conversationalist",
            "description": "Completed 10 conversations",
            "icon": "💬",
            "points": 40
        },
        "fifty_conversations": {
            "title": "Language Enthusiast",
            "description": "Completed 50 conversations",
            "icon": "🌟",
            "points": 100
        },
        "hundred_conversations": {
            "title": "Language Expert",
            "description": "Completed 100 conversations",
            "icon": "🏆",
            "points": 250
        }
    }
    
    async def calculate_conversation_points(
        self,
        pronunciation_score: float,
        error_count: int,
        session_duration_seconds: float
    ) -> int:
        """
        Calculate points earned from a single conversation
        Args:
            pronunciation_score: Score from 0-100
            error_count: Number of errors made
            session_duration_seconds: Length of conversation
        Returns:
            Points earned
        """
        base_points = 5  # Base points for completing a conversation
        
        # Pronunciation bonus (0-10 points)
        pronunciation_bonus = int(pronunciation_score / 10)
        
        # Error penalty (max -5 points)
        error_penalty = min(error_count * 1, 5)
        
        # Duration bonus (1 point per 30 seconds, max 10 points)
        duration_bonus = min(int(session_duration_seconds / 30), 10)
        
        total_points = max(base_points + pronunciation_bonus - error_penalty + duration_bonus, 1)
        return total_points
    
    async def check_and_award_achievements(
        self,
        user_id: str,
        conversation_data: Dict
    ) -> List[AchievementModel]:
        """
        Check if user earned any new achievements and award them
        Args:
            user_id: Firebase UID
            conversation_data: Data from the completed conversation
        Returns:
            List of newly awarded achievements
        """
        new_achievements = []
        
        # Get user progress
        progress = await ProgressRepository.get_or_create_progress(user_id)
        user = await UserRepository.get_user_by_firebase_uid(user_id)
        
        if not user:
            return new_achievements
        
        # Check first conversation
        if progress.total_conversations == 1:
            achievement = AchievementModel(
                user_id=user_id,
                achievement_type="first_conversation",
                **self.ACHIEVEMENTS["first_conversation"]
            )
            await AchievementRepository.award_achievement(achievement)
            await UserRepository.increment_points(user_id, self.ACHIEVEMENTS["first_conversation"]["points"])
            new_achievements.append(achievement)
        
        # Check conversation milestones
        if progress.total_conversations == 10:
            achievement = AchievementModel(
                user_id=user_id,
                achievement_type="ten_conversations",
                **self.ACHIEVEMENTS["ten_conversations"]
            )
            await AchievementRepository.award_achievement(achievement)
            await UserRepository.increment_points(user_id, self.ACHIEVEMENTS["ten_conversations"]["points"])
            new_achievements.append(achievement)
        
        elif progress.total_conversations == 50:
            achievement = AchievementModel(
                user_id=user_id,
                achievement_type="fifty_conversations",
                **self.ACHIEVEMENTS["fifty_conversations"]
            )
            await AchievementRepository.award_achievement(achievement)
            await UserRepository.increment_points(user_id, self.ACHIEVEMENTS["fifty_conversations"]["points"])
            new_achievements.append(achievement)
        
        elif progress.total_conversations == 100:
            achievement = AchievementModel(
                user_id=user_id,
                achievement_type="hundred_conversations",
                **self.ACHIEVEMENTS["hundred_conversations"]
            )
            await AchievementRepository.award_achievement(achievement)
            await UserRepository.increment_points(user_id, self.ACHIEVEMENTS["hundred_conversations"]["points"])
            new_achievements.append(achievement)
        
        # Check pronunciation master
        pronunciation_score = conversation_data.get("pronunciation_score", 0)
        if pronunciation_score >= 90:
            achievement = AchievementModel(
                user_id=user_id,
                achievement_type="pronunciation_master",
                **self.ACHIEVEMENTS["pronunciation_master"],
                metadata={"score": pronunciation_score}
            )
            await AchievementRepository.award_achievement(achievement)
            await UserRepository.increment_points(user_id, self.ACHIEVEMENTS["pronunciation_master"]["points"])
            new_achievements.append(achievement)
        
        # Check error-free conversation
        if conversation_data.get("error_count", 0) == 0:
            achievement = AchievementModel(
                user_id=user_id,
                achievement_type="error_free",
                **self.ACHIEVEMENTS["error_free"]
            )
            await AchievementRepository.award_achievement(achievement)
            await UserRepository.increment_points(user_id, self.ACHIEVEMENTS["error_free"]["points"])
            new_achievements.append(achievement)
        
        # Check streak achievements
        if user.current_streak == 7:
            achievement = AchievementModel(
                user_id=user_id,
                achievement_type="week_streak",
                **self.ACHIEVEMENTS["week_streak"]
            )
            await AchievementRepository.award_achievement(achievement)
            await UserRepository.increment_points(user_id, self.ACHIEVEMENTS["week_streak"]["points"])
            new_achievements.append(achievement)
        
        elif user.current_streak == 30:
            achievement = AchievementModel(
                user_id=user_id,
                achievement_type="month_streak",
                **self.ACHIEVEMENTS["month_streak"]
            )
            await AchievementRepository.award_achievement(achievement)
            await UserRepository.increment_points(user_id, self.ACHIEVEMENTS["month_streak"]["points"])
            new_achievements.append(achievement)
        
        return new_achievements
    
    async def update_user_streak(self, user_id: str) -> Dict:
        """
        Update user's practice streak
        Returns current streak information
        """
        return await StreakRepository.update_streak(user_id)


gamification_service = GamificationService()
