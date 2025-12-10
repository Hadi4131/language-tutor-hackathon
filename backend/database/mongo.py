from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class Database:
    client: AsyncIOMotorClient = None

    def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        print("Connected to MongoDB Atlas")

    def close(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB Atlas")

    def get_db(self):
         # Assuming database name is 'language_learning_db', you can also make this configurable
        return self.client.language_learning_db

db = Database()

async def get_database():
    return db.get_db()
