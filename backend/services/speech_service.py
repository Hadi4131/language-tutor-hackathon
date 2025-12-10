from google.cloud import speech
from typing import Dict
from core.config import settings

class SpeechService:
    def __init__(self):
        self.client = speech.SpeechClient()

    async def transcribe_audio(self, audio_content: bytes) -> Dict:
        """
        Transcribes audio content to text using Google Speech-to-Text.
        Returns both transcript and word-level confidence scores for pronunciation analysis.
        """
        audio = speech.RecognitionAudio(content=audio_content)
        
        # Configure for best results with language learning
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            enable_word_confidence=True,  # Enable word-level confidence scores
            enable_word_time_offsets=True,  # Useful for detailed analysis
        )

        try:
            response = self.client.recognize(config=config, audio=audio)
            
            transcript = ""
            word_confidences = []
            
            for result in response.results:
                alternative = result.alternatives[0]
                transcript += alternative.transcript
                
                # Extract word-level confidence scores
                for word_info in alternative.words:
                    word = word_info.word
                    confidence = word_info.confidence
                    word_confidences.append((word, confidence))
            
            return {
                "transcript": transcript,
                "word_confidences": word_confidences,
                "confidence": result.alternatives[0].confidence if response.results else 0.0
            }
        except Exception as e:
            print(f"Error extracting text from audio: {e}")
            raise e

speech_service = SpeechService()
