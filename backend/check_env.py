from core.config import settings

print("Checking environment variables...")
print("=" * 60)

print(f"\nELEVENLABS_API_KEY: {settings.ELEVENLABS_API_KEY[:20]}..." if settings.ELEVENLABS_API_KEY else "Not set")
print(f"Key length: {len(settings.ELEVENLABS_API_KEY)}")
print(f"Key starts with 'sk_': {settings.ELEVENLABS_API_KEY.startswith('sk_')}")

# Check if it matches what's in the file
expected_start = "sk_452b3c1091f187d413c6fc4befb147dccc00b6455d239af1"
actual = settings.ELEVENLABS_API_KEY

if actual == expected_start:
    print(f"\n✅ Key matches the .env file")
else:
    print(f"\n⚠️ Key doesn't match! Expected: {expected_start[:20]}...")
    print(f"   Got: {actual[:20]}...")
