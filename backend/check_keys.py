from core.config import settings

print(f"GOOGLE_API_KEY: {settings.GOOGLE_API_KEY[:20]}..." if settings.GOOGLE_API_KEY else "GOOGLE_API_KEY: Not set")
print(f"VERTEX_API_KEY: {settings.VERTEX_API_KEY[:20]}..." if settings.VERTEX_API_KEY else "VERTEX_API_KEY: Not set")

# Test which one is being used
api_key = settings.VERTEX_API_KEY or settings.GOOGLE_API_KEY
print(f"\nUsing API Key: {api_key[:20]}...")
print(f"Key length: {len(api_key)}")
