import pymongo
from pymongo import MongoClient

import os

class MongoDBTriggerEmojis:

    def __init__(self, collection) -> None:
        self.collection = collection

    def insert(self, guild_id, emoji):
        return self.collection.insert_one({"_id":guild_id, "emoji":emoji})
    
    def get(self, guild_id, default):
        tup = tuple(self.collection.find({"_id":guild_id}))
        if tup:
            return tup[0]["emoji"]
        else:
            return default
    
    def update(self, guild_id, emoji):
        return self.collection.update_one({"_id":guild_id}, {"$set":{"emoji":emoji}})
    
    def exists(self, guild_id):
        return self.collection.count_documents({"_id":guild_id}) > 0


from dotenv import load_dotenv
load_dotenv()

client = pymongo.MongoClient(url := os.getenv("MONGO_URL"))
print("Connected to database.")
database = client["codegod"]
collection = database["trigger_emojis"]

trigger_emojis = MongoDBTriggerEmojis(collection)


