import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    ELEVENLABS_API_KEY: str
    MONGODB_URI: str
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    FIREBASE_ADMIN_SDK_PATH: str = "./firebase-admin-sdk.json"
    
    class Config:
        case_sensitive = True

settings = Settings()
