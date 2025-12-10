from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId


class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    firebase_uid: str
    email: str
    display_name: Optional[str] = None
    level: str = "beginner"
    target_language: str = "en-US"
    preferred_personality: str = "friendly"
    total_points: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_practice_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    settings: Dict = Field(default_factory=dict)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class ErrorDetail(BaseModel):
    error_type: str
    incorrect_word: str
    correct_word: str
    explanation: str


class ConversationHistoryModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    transcript: str
    corrected_sentence: str
    errors: List[ErrorDetail] = []
    learning_tip: str
    follow_up_question: str
    feedback_tone: str
    detected_emotion: Optional[str] = None
    emotional_feedback: Optional[str] = None
    pronunciation_score: Optional[float] = None
    word_confidence_scores: Optional[Dict[str, float]] = None
    problematic_phonemes: Optional[List[str]] = None
    cultural_context: Optional[str] = None
    ai_personality_used: str = "friendly"
    session_duration_seconds: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class PronunciationProgress(BaseModel):
    phoneme: str
    scores: List[float] = []
    last_practice_date: datetime
    improvement_percentage: float = 0.0


class ProgressTrackingModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    pronunciation_progress: Dict[str, PronunciationProgress] = {}
    overall_pronunciation_score: float = 0.0
    common_errors: Dict[str, int] = {}
    recent_improvements: List[str] = []
    total_conversations: int = 0
    total_practice_time_minutes: float = 0.0
    average_session_duration: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class AchievementModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    achievement_type: str
    title: str
    description: str
    icon: str
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class StreakModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    current_streak: int = 0
    longest_streak: int = 0
    last_practice_date: Optional[datetime] = None
    streak_history: List[datetime] = []

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class LeaderboardEntry(BaseModel):
    user_id: str
    display_name: str
    total_points: int
    current_streak: int
    rank: int
    country: Optional[str] = None
    age_group: Optional[str] = None


class PersonalityProfile(BaseModel):
    id: str
    name: str
    description: str
    teaching_style: str
    sample_response: str
    avatar_emoji: str
    system_prompt_modifier: str
