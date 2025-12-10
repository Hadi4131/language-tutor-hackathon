import google.generativeai as genai
from core.config import settings

def list_models():
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    print("Listing available Gemini models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name} (Display Name: {m.display_name})")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
