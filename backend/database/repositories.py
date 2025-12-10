from datetime import datetime, timedelta
from typing import List, Optional, Dict
from database.models import (
    UserModel, ConversationHistoryModel, ProgressTrackingModel,
    AchievementModel, StreakModel, LeaderboardEntry
)
from database.mongo import get_database


class UserRepository:
    @staticmethod
    async def create_user(user: UserModel) -> str:
        db = await get_database()
        result = await db.users.insert_one(user.dict(by_alias=True, exclude={"id"}))
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_by_firebase_uid(firebase_uid: str) -> Optional[UserModel]:
        db = await get_database()
        user_data = await db.users.find_one({"firebase_uid": firebase_uid})
        if user_data:
            return UserModel(**user_data)
        return None
    
    @staticmethod
    async def update_user(firebase_uid: str, update_data: Dict) -> bool:
        db = await get_database()
        result = await db.users.update_one(
            {"firebase_uid": firebase_uid},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def increment_points(firebase_uid: str, points: int) -> bool:
        db = await get_database()
        result = await db.users.update_one(
            {"firebase_uid": firebase_uid},
            {"$inc": {"total_points": points}}
        )
        return result.modified_count > 0


class ConversationRepository:
    @staticmethod
    async def save_conversation(conversation: ConversationHistoryModel) -> str:
        db = await get_database()
        result = await db.conversations.insert_one(conversation.dict(by_alias=True, exclude={"id"}))
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_conversations(user_id: str, limit: int = 50) -> List[ConversationHistoryModel]:
        db = await get_database()
        cursor = db.conversations.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        conversations = await cursor.to_list(length=limit)
        return [ConversationHistoryModel(**conv) for conv in conversations]
    
    @staticmethod
    async def get_recent_errors(user_id: str, days: int = 7) -> List[Dict]:
        """Get recent error patterns for analysis"""
        db = await get_database()
        date_threshold = datetime.utcnow() - timedelta(days=days)
        cursor = db.conversations.find({
            "user_id": user_id,
            "created_at": {"$gte": date_threshold}
        })
        conversations = await cursor.to_list(length=100)
        
        error_counts = {}
        for conv in conversations:
            for error in conv.get("errors", []):
                error_type = error.get("error_type", "other")
                error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return error_counts


class ProgressRepository:
    @staticmethod
    async def get_or_create_progress(user_id: str) -> ProgressTrackingModel:
        db = await get_database()
        progress_data = await db.progress.find_one({"user_id": user_id})
        
        if progress_data:
            return ProgressTrackingModel(**progress_data)
        else:
            # Create new progress tracking
            new_progress = ProgressTrackingModel(user_id=user_id)
            await db.progress.insert_one(new_progress.dict(by_alias=True, exclude={"id"}))
            return new_progress
    
    @staticmethod
    async def update_pronunciation_progress(user_id: str, phoneme: str, score: float) -> bool:
        db = await get_database()
        
        # Get current progress
        progress = await ProgressRepository.get_or_create_progress(user_id)
        
        # Update phoneme-specific progress
        phoneme_key = f"pronunciation_progress.{phoneme}"
        result = await db.progress.update_one(
            {"user_id": user_id},
            {
                "$push": {f"{phoneme_key}.scores": score},
                "$set": {
                    f"{phoneme_key}.last_practice_date": datetime.utcnow(),
                    f"{phoneme_key}.phoneme": phoneme,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        return result.modified_count > 0 or result.upserted_id is not None
    
    @staticmethod
    async def increment_conversation_count(user_id: str) -> bool:
        db = await get_database()
        result = await db.progress.update_one(
            {"user_id": user_id},
            {
                "$inc": {"total_conversations": 1},
                "$set": {"updated_at": datetime.utcnow()}
            },
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None


class AchievementRepository:
    @staticmethod
    async def award_achievement(achievement: AchievementModel) -> str:
        db = await get_database()
        
        # Check if already earned
        existing = await db.achievements.find_one({
            "user_id": achievement.user_id,
            "achievement_type": achievement.achievement_type
        })
        
        if existing:
            return str(existing["_id"])  # Already earned
        
        result = await db.achievements.insert_one(achievement.dict(by_alias=True, exclude={"id"}))
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_achievements(user_id: str) -> List[AchievementModel]:
        db = await get_database()
        cursor = db.achievements.find({"user_id": user_id}).sort("earned_at", -1)
        achievements = await cursor.to_list(length=100)
        return [AchievementModel(**ach) for ach in achievements]


class StreakRepository:
    @staticmethod
    async def update_streak(user_id: str) -> Dict:
        """Update user's streak and return current streak info"""
        db = await get_database()
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        streak_data = await db.streaks.find_one({"user_id": user_id})
        
        if not streak_data:
            # First time practicing
            new_streak = StreakModel(
                user_id=user_id,
                current_streak=1,
                longest_streak=1,
                last_practice_date=now,
                streak_history=[today]
            )
            await db.streaks.insert_one(new_streak.dict(by_alias=True, exclude={"id"}))
            return {"current_streak": 1, "longest_streak": 1, "streak_maintained": True}
        
        last_practice = streak_data.get("last_practice_date")
        if last_practice:
            last_practice_day = last_practice.replace(hour=0, minute=0, second=0, microsecond=0)
            
            if last_practice_day == today:
                # Already practiced today
                return {
                    "current_streak": streak_data.get("current_streak", 1),
                    "longest_streak": streak_data.get("longest_streak", 1),
                    "streak_maintained": True
                }
            elif last_practice_day == today - timedelta(days=1):
                # Practiced yesterday, increment streak
                new_current = streak_data.get("current_streak", 0) + 1
                new_longest = max(new_current, streak_data.get("longest_streak", 0))
                
                await db.streaks.update_one(
                    {"user_id": user_id},
                    {
                        "$set": {
                            "current_streak": new_current,
                            "longest_streak": new_longest,
                            "last_practice_date": now
                        },
                        "$push": {"streak_history": today}
                    }
                )
                
                # Also update user model
                await db.users.update_one(
                    {"firebase_uid": user_id},
                    {
                        "$set": {
                            "current_streak": new_current,
                            "longest_streak": new_longest,
                            "last_practice_date": now
                        }
                    }
                )
                
                return {"current_streak": new_current, "longest_streak": new_longest, "streak_maintained": True}
            else:
                # Streak broken, reset
                await db.streaks.update_one(
                    {"user_id": user_id},
                    {
                        "$set": {
                            "current_streak": 1,
                            "last_practice_date": now
                        },
                        "$push": {"streak_history": today}
                    }
                )
                
                await db.users.update_one(
                    {"firebase_uid": user_id},
                    {"$set": {"current_streak": 1, "last_practice_date": now}}
                )
                
                return {
                    "current_streak": 1,
                    "longest_streak": streak_data.get("longest_streak", 1),
                    "streak_maintained": False
                }
        
        return {"current_streak": 1, "longest_streak": 1, "streak_maintained": True}


class LeaderboardRepository:
    @staticmethod
    async def get_global_leaderboard(limit: int = 100) -> List[LeaderboardEntry]:
        db = await get_database()
        cursor = db.users.find().sort("total_points", -1).limit(limit)
        users = await cursor.to_list(length=limit)
        
        leaderboard = []
        for rank, user in enumerate(users, start=1):
            entry = LeaderboardEntry(
                user_id=user.get("firebase_uid"),
                display_name=user.get("display_name", "Anonymous"),
                total_points=user.get("total_points", 0),
                current_streak=user.get("current_streak", 0),
                rank=rank,
                country=user.get("settings", {}).get("country"),
                age_group=user.get("settings", {}).get("age_group")
            )
            leaderboard.append(entry)
        
        return leaderboard
    
    @staticmethod
    async def get_user_rank(user_id: str) -> Optional[int]:
        """Get user's current rank"""
        db = await get_database()
        user = await db.users.find_one({"firebase_uid": user_id})
        if not user:
            return None
        
        user_points = user.get("total_points", 0)
        count = await db.users.count_documents({"total_points": {"$gt": user_points}})
        return count + 1
