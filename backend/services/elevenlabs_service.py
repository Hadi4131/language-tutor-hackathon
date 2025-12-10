from elevenlabs.client import ElevenLabs
from core.config import settings

class ElevenLabsService:
    def __init__(self):
        self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

    async def generate_audio(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
        """
        Generates audio from text using ElevenLabs.
        Returns audio bytes (MP3).
        """
        try:
            # Using text_to_speech.convert which returns a generator
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2"
            )
            
            # Combine the chunks into a single bytes object
            audio_bytes = b"".join(chunk for chunk in audio_generator)
            return audio_bytes
        except Exception as e:
            print(f"Error generating audio with ElevenLabs: {e}")
            raise e

elevenlabs_service = ElevenLabsService()
