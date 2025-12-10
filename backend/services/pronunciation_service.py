from typing import Dict, List, Optional, Tuple
import statistics


class PronunciationService:
    """
    Service for analyzing pronunciation quality and tracking improvement
    """
    
    # Common problematic phonemes for language learners
    PHONEME_PATTERNS = {
        "th": ["the", "that", "this", "think", "three", "mother", "father"],
        "r": ["red", "right", "very", "carry", "area"],
        "l": ["light", "little", "tell", "people"],
        "v": ["very", "have", "voice", "every"],
        "w": ["when", "where", "what", "which"],
        "ch": ["check", "church", "teacher", "much"],
        "sh": ["she", "should", "fish", "wash"],
    }
    
    def calculate_pronunciation_score(
        self, 
        word_confidences: List[Tuple[str, float]]
    ) -> float:
        """
        Calculate overall pronunciation score (0-100) based on word confidence scores
        Args:
            word_confidences: List of (word, confidence) tuples from Speech-to-Text
        Returns:
            Score from 0-100
        """
        if not word_confidences:
            return 50.0  # Neutral score
        
        # Extract confidence values
        confidences = [conf for _, conf in word_confidences]
        
        # Calculate weighted average (higher confidence = better pronunciation)
        avg_confidence = statistics.mean(confidences)
        
        # Convert to 0-100 scale (Speech-to-Text confidence is typically 0.0-1.0)
        score = avg_confidence * 100
        
        return round(score, 2)
    
    def identify_problematic_phonemes(
        self, 
        word_confidences: List[Tuple[str, float]],
        threshold: float = 0.7
    ) -> List[str]:
        """
        Identify phonemes that the user struggles with
        Args:
            word_confidences: List of (word, confidence) tuples
            threshold: Confidence threshold below which a phoneme is problematic
        Returns:
            List of problematic phoneme identifiers
        """
        problematic = set()
        
        for word, confidence in word_confidences:
            if confidence < threshold:
                # Check which phonemes this word contains
                word_lower = word.lower()
                for phoneme, patterns in self.PHONEME_PATTERNS.items():
                    if any(pattern in word_lower for pattern in patterns):
                        problematic.add(phoneme)
        
        return list(problematic)
    
    def calculate_improvement(
        self, 
        historical_scores: List[float],
        recent_scores: List[float]
    ) -> float:
        """
        Calculate improvement percentage between historical and recent scores
        Args:
            historical_scores: Old scores (e.g., from last week)
            recent_scores: Recent scores (e.g., from this week)
        Returns:
            Improvement percentage (can be negative if scores declined)
        """
        if not historical_scores or not recent_scores:
            return 0.0
        
        historical_avg = statistics.mean(historical_scores)
        recent_avg = statistics.mean(recent_scores)
        
        if historical_avg == 0:
            return 0.0
        
        improvement = ((recent_avg - historical_avg) / historical_avg) * 100
        return round(improvement, 1)
    
    def generate_pronunciation_feedback(
        self,
        score: float,
        problematic_phonemes: List[str]
    ) -> str:
        """
        Generate human-friendly pronunciation feedback
        Args:
            score: Overall pronunciation score (0-100)
            problematic_phonemes: List of phonemes user struggles with
        Returns:
            Feedback message
        """
        feedback_parts = []
        
        # Overall score feedback
        if score >= 90:
            feedback_parts.append("Excellent pronunciation! 🌟")
        elif score >= 75:
            feedback_parts.append("Great job! Your pronunciation is clear.")
        elif score >= 60:
            feedback_parts.append("Good effort! Let's work on clarity.")
        else:
            feedback_parts.append("Keep practicing! Pronunciation takes time.")
        
        # Specific phoneme feedback
        if problematic_phonemes:
            phoneme_list = ", ".join([f"'{p}'" for p in problematic_phonemes[:3]])
            feedback_parts.append(f"Focus on improving: {phoneme_list} sounds.")
        
        return " ".join(feedback_parts)
    
    def get_practice_suggestions(self, phoneme: str) -> List[str]:
        """
        Get practice word suggestions for a specific phoneme
        Args:
            phoneme: Phoneme identifier (e.g., "th", "r")
        Returns:
            List of practice words
        """
        return self.PHONEME_PATTERNS.get(phoneme, [])


pronunciation_service = PronunciationService()
