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

    def get_voices(self):
        """
        Fetches available voices from ElevenLabs.
        """
        try:
            # User provided specific voices
            target_voices = {
                "jqcCZkN6Knx8BJ5TBdYR": {"name": "Zara", "category": "American Female", "description": "Professional"},
                "yj30vwTGJxSHezdAGsv9": {"name": "Jessa", "category": "American Female", "description": "Friendly"},
                "j9jfwdrw7BRfcR43Qohk": {"name": "Frederick Surrey", "category": "British Male", "description": "Formal"},
                "kPzsL2i3teMYv0FxEYQ6": {"name": "Britteny", "category": "American Female", "description": "Energetic"},
                "a1TnjruAs5jTzdrjL8Vd": {"name": "Frank", "category": "American Male", "description": "Deep"},
                "qyFhaJEAwHR0eYLCmlUT": {"name": "Matt", "category": "American Male", "description": "Casual"}
            }

            try:
                response = self.client.voices.get_all()
                print(f"DEBUG: Found {len(response.voices)} voices in ElevenLabs account.")
                
                # 1. Try to find the target voices in the API response
                for voice in response.voices:
                    if voice.voice_id in target_voices:
                        print(f"DEBUG: Found target voice {voice.name} ({voice.voice_id})")
                        target_info = target_voices[voice.voice_id]
                        voices.append({
                            "voice_id": voice.voice_id,
                            "name": target_info["name"],
                            "category": voice.category or target_info["category"],
                            "description": voice.description or target_info["description"],
                            "preview_url": voice.preview_url
                        })
            except Exception as api_error:
                print(f"Error fetching voices from ElevenLabs API (using fallback): {api_error}")

            # 2. Always run fallback: If any are missing (or API failed), add them manually
            found_ids = [v["voice_id"] for v in voices]
            for vid, info in target_voices.items():
                if vid not in found_ids:
                    print(f"DEBUG: Target voice {info['name']} not in current list. Adding manually.")
                    voices.append({
                        "voice_id": vid,
                        "name": info["name"],
                        "category": info["category"],
                        "description": info["description"],
                        "preview_url": "" 
                    })

            print(f"DEBUG: Returning {len(voices)} voices.")
            return voices
        except Exception as e:
            print(f"Critical error in get_voices: {e}")
            # Even in critical error, try to return the hardcoded list
            return [
                {"voice_id": vid, "name": info["name"], "category": info["category"], "description": info["description"], "preview_url": ""}
                for vid, info in target_voices.items()
            ]

elevenlabs_service = ElevenLabsService()
