import google.generativeai as genai
import json
from core.config import settings

class GeminiService:
    def __init__(self):
        api_key = settings.VERTEX_API_KEY or settings.GOOGLE_API_KEY
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
        Simplified for faster responses.
        """
        
        prompt = f"""
        You are an English tutor. Analyze this sentence: "{user_text}"
        
        Provide a JSON response (no markdown):
        {{
            "corrected_sentence": "The corrected sentence",
            "errors": [],
            "learning_tip": "One short tip",
            "follow_up_question": "A question"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            text_response = response.text.strip()
            
            if text_response.startswith("```json"):
                text_response = text_response[7:-3]
            elif text_response.startswith("```"):
                 text_response = text_response[3:-3]
            
            analysis = json.loads(text_response)
            analysis['feedback_tone'] = 'encouraging'
            analysis['detected_emotion'] = 'neutral'
            analysis['emotional_feedback'] = ''
            analysis['cultural_context'] = ''
            
            return analysis
        except Exception as e:
            print(f"Error: {e}")
            return {
                "corrected_sentence": user_text,
                "errors": [],
                "learning_tip": "Keep practicing!",
                "follow_up_question": "Could you say that again?",
                "feedback_tone": "neutral",
                "detected_emotion": "neutral",
                "emotional_feedback": "",
                "cultural_context": ""
            }

gemini_service = GeminiService()
