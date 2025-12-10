from database.models import UserModel
from database.repositories import UserRepository
import asyncio


async def create_demo_user():
    """Create a demo user for testing"""
    
    demo_user = UserModel(
        firebase_uid="demo_user_123",
        email="demo@languagetutor.com",
        display_name="Demo User",
        level="intermediate",
        target_language="en-US",
        preferred_personality="friendly",
    )
    
    try:
        user_id = await UserRepository.create_user(demo_user)
        print(f"✅ Demo user created successfully with ID: {user_id}")
        print(f"   Email: {demo_user.email}")
        print(f"   Display Name: {demo_user.display_name}")
        print(f"   Level: {demo_user.level}")
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        print("   User may already exist")


if __name__ == "__main__":
    from database.mongo import db
    
    # Connect to database
    db.connect()
    
    # Create demo user
    asyncio.run(create_demo_user())
    
    # Close connection
    db.close()
