import motor.motor_asyncio

import os

class MongoDBTriggerEmojis:

    def __init__(self, collection) -> None:
        self.collection = collection

    async def insert(self, guild_id, emoji):
        return await self.collection.insert_one({"_id":guild_id, "emoji":emoji})
    
    async def get(self, guild_id, default):
        async for document in self.collection.find({"_id":guild_id}):
            if "emoji" in document:
                return document["emoji"]
        return default
    
    async def update(self, guild_id, emoji):
        return await self.collection.update_one({"_id":guild_id}, {"$set":{"emoji":emoji}})
    
    async def exists(self, guild_id):
        return (await self.collection.count_documents({"_id":guild_id})) > 0


from dotenv import load_dotenv
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))
print("Connected to database.")
database = client["codegod"]
collection = database["trigger_emojis"]

trigger_emojis = MongoDBTriggerEmojis(collection)


