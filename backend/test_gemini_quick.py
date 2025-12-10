import asyncio
from services.gemini_service import gemini_service

async def test():
    print("Testing gemini-2.5-flash...")
    result = await gemini_service.analyze_language("Yesterday I go to the store")
    
    if result.get("learning_tip") == "Could not analyze at this moment.":
        print("❌ FAILED: Returned fallback response")
    else:
        print("✅ SUCCESS!")
        print(f"Corrected: {result.get('corrected_sentence')}")
        print(f"Tip: {result.get('learning_tip')}")
        print(f"Follow-up: {result.get('follow_up_question')}")

if __name__ == "__main__":
    asyncio.run(test())
