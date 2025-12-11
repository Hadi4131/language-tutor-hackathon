import google.generativeai as genai
import json
from core.config import settings

class GeminiService:
    def __init__(self):
        api_key = settings.GOOGLE_API_KEY
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def analyze_language(
        self, 
        user_text: str, 
        user_level: str = "intermediate",
        personality: str = "friendly",
        conversation_history: list = None
    ) -> dict:
        """
        Analyzes user text for grammar and vocabulary using Gemini.
        Enhanced with personalized, context-aware responses.
        """
        
        # Personality tone mapping for more natural responses
        personality_tones = {
            "friendly": "warm, encouraging, and supportive like a helpful friend",
            "professional": "clear, precise, and constructive like a skilled teacher", 
            "enthusiastic": "energetic, positive, and motivational like an excited coach",
            "patient": "calm, reassuring, and understanding like a caring mentor"
        }
        
        # Get the appropriate tone based on personality parameter
        tone = personality_tones.get(personality, "friendly")
        
        # Build context from conversation history if available
        context = ""
        if conversation_history and len(conversation_history) > 0:
            context = "Previous conversation:\n"
            for msg in conversation_history[-3:]:  # Last 3 messages for context
                speaker = "Student" if msg.get("role") == "user" else "Tutor"
                context += f"{speaker}: {msg.get('content', '')}\n"
            context += "\n"
        
        # Enhanced prompt with context awareness
        prompt = f"""
        ROLE: You are an adaptive English conversation tutor. The student is at the '{user_level}' level.
        PERSONALITY: Be {tone}. Sound natural and human-like, not robotic.
        
        {context}
        
        CURRENT STUDENT SENTENCE: "{user_text}"
        
        CRITICAL INSTRUCTIONS:
        1. First, check if the sentence has any grammar, vocabulary, or pronunciation issues.
        2. If perfect, acknowledge it positively and ask a RELEVANT, OPEN-ENDED question based on content.
        3. If there are errors, correct them gently and ask a related question.
        4. NEVER ask "Could you say that again?" or "Repeat that please" unless audio was truly unintelligible.
        5. Base your follow-up question on WHAT the student said to continue a natural conversation.
        
        EXAMPLES OF GOOD RESPONSES:
        - Student: "Hello" → "Hi there! How's your day going?"
        - Student: "I like pizza" → "Me too! What's your favorite pizza topping?"
        - Student: "Yesterday I go park" → "Good try! It's 'Yesterday I went to the park.' What did you do there?"
        - Student: "The weather is good" → "Yes, it is! What do you like to do on nice days like this?"
        
        RESPONSE FORMAT (JSON ONLY, no markdown or additional text):
        {{
            "corrected_sentence": "The grammatically correct version (same as input if perfect)",
            "errors": [
                {{
                    "type": "grammar/vocabulary/pronunciation",
                    "incorrect": "the incorrect word/phrase",
                    "correct": "the correction",
                    "explanation": "brief, clear explanation"
                }}
            ],
            "learning_tip": "One specific, helpful tip matching the user's level",
            "follow_up_question": "A natural, engaging question based on their sentence content",
            "conversation_continuity": "How this relates to previous context (if any)"
        }}
        
        REMEMBER: Keep responses concise but natural. The goal is engaging conversation practice.
        """
        
        try:
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            text_response = response.text.strip()
            
            # Clean JSON response (remove markdown code blocks if present)
            if text_response.startswith("```json"):
                text_response = text_response[7:-3]
            elif text_response.startswith("```"):
                text_response = text_response[3:-3]
            
            # Parse the JSON response
            analysis = json.loads(text_response)
            
            # Add additional metadata for your app
            analysis['feedback_tone'] = personality
            analysis['user_level'] = user_level
            analysis['detected_emotion'] = self._detect_emotion(user_text)
            analysis['emotional_feedback'] = self._get_emotional_feedback(analysis['detected_emotion'])
            analysis['cultural_context'] = self._add_cultural_context(user_text)
            
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}. Response was: {text_response}")
            # Fallback with intelligent context
            return self._get_fallback_response(user_text, user_level, personality)
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return self._get_fallback_response(user_text, user_level, personality)
    
    def _detect_emotion(self, text: str) -> str:
        """Simple emotion detection based on keywords"""
        text_lower = text.lower()
        positive_words = ['happy', 'good', 'great', 'excited', 'love', 'like', 'wonderful']
        negative_words = ['sad', 'bad', 'angry', 'hate', 'tired', 'difficult']
        
        for word in positive_words:
            if word in text_lower:
                return "positive"
        for word in negative_words:
            if word in text_lower:
                return "negative"
        return "neutral"
    
    def _get_emotional_feedback(self, emotion: str) -> str:
        """Get appropriate feedback based on detected emotion"""
        feedbacks = {
            "positive": "I can tell you're in a good mood! 😊",
            "negative": "It's okay to feel that way. Let's practice together. 💪",
            "neutral": "Let's continue our conversation!"
        }
        return feedbacks.get(emotion, "")
    
    def _add_cultural_context(self, text: str) -> str:
        """Add cultural notes for specific topics"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['pizza', 'food', 'eat']):
            return "In English-speaking countries, people often discuss food preferences in casual conversation."
        elif any(word in text_lower for word in ['weather', 'sunny', 'rain']):
            return "Talking about weather is a common small talk topic in many English-speaking cultures."
        elif any(word in text_lower for word in ['hello', 'hi', 'greeting']):
            return "In English, 'hello' is standard, but 'hi' or 'hey' are more casual with friends."
        return ""
    
    def _get_fallback_response(self, user_text: str, user_level: str, personality: str) -> dict:
        """Intelligent fallback when Gemini fails"""
        # Simple correction for common errors
        corrections = {
            "i go": "I went",
            "i is": "I am",
            "she do": "she does",
            "they was": "they were"
        }
        
        corrected = user_text
        errors = []
        
        for wrong, right in corrections.items():
            if wrong in user_text.lower():
                corrected = user_text.lower().replace(wrong, right).capitalize()
                errors.append({
                    "type": "grammar",
                    "incorrect": wrong,
                    "correct": right,
                    "explanation": f"Use '{right}' for past tense/agreement"
                })
        
        # Level-appropriate tips
        level_tips = {
            "beginner": "Great start! Try using complete sentences with subjects and verbs.",
            "intermediate": "Good progress! Experiment with different tenses and connectors.",
            "advanced": "Excellent! Work on natural phrasing and idiomatic expressions."
        }
        
        # Context-aware follow-up questions
        follow_up_questions = {
            "hello": "What would you like to talk about today?",
            "how are you": "I'm doing well! How about you?",
            "i like": "That's interesting! Why do you like that?",
            "i want": "That's a good goal! How can you achieve it?"
        }
        
        # Find the best follow-up question
        follow_up = "Could you tell me more about that?"
        for key, question in follow_up_questions.items():
            if key in user_text.lower():
                follow_up = question
                break
        
        return {
            "corrected_sentence": corrected,
            "errors": errors,
            "learning_tip": level_tips.get(user_level, "Keep practicing!"),
            "follow_up_question": follow_up,
            "feedback_tone": personality,
            "detected_emotion": "neutral",
            "emotional_feedback": "",
            "cultural_context": "",
            "conversation_continuity": "Continuing our practice session"
        }

# Singleton instance
gemini_service = GeminiService()
