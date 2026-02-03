import time
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

import re

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        
        # Collections
        self.index_cache = self.db.index_cache
        self.users = self.db.users
        self.favorites = self.db.favorites
        self.trending = self.db.trending
        self.ads_cooldown = self.db.ads_cooldown
        self.settings = self.db.settings

    # --- INDEX CACHE ---
    async def save_file(self, file_data):
        # file_data: anime_name, season, episode, quality, audio, message_id, channel_id, file_unique_id
        file_data['added_at'] = time.time()
        file_data['is_new'] = True
        
        # Update if exists (same file/quality) or insert
        await self.index_cache.update_one(
            {
                "anime_name": file_data["anime_name"],
                "season": file_data["season"],
                "episode": file_data["episode"],
                "quality": file_data["quality"]
            },
            {"$set": file_data},
            upsert=True
        )

    async def get_anime_list(self):
        return await self.index_cache.distinct("anime_name")

    async def search_anime(self, query):
        # Regex search for anime name
        # Escape special characters to prevent regex errors (e.g. unmatched parenthesis)
        escaped_query = re.escape(query)
        regex = {"$regex": escaped_query, "$options": "i"}

        cursor = self.index_cache.find({"anime_name": regex})
        # Distinct is tricky with find, so we aggregate or just python set
        # Using aggregation for cleaner distinct + match
        pipeline = [
            {"$match": {"anime_name": regex}},
            {"$group": {"_id": "$anime_name"}},
            {"$limit": 50}
        ]
        results = []
        async for doc in self.index_cache.aggregate(pipeline):
            results.append(doc["_id"])
        return results

    async def get_seasons(self, anime_name):
        return await self.index_cache.find({"anime_name": anime_name}).distinct("season")

    async def get_episodes(self, anime_name, season):
        cursor = self.index_cache.find({
            "anime_name": anime_name,
            "season": season
        }).sort("episode", 1)
        return await cursor.to_list(length=None)
        
    async def get_file(self, file_id_str):
        # We might need to store a unique ID reference for the deep link
        # Prompt implies browsing. deep link probably sends a unique ID (like ObjectId hex)
        # Let's assume we pass the Object ID
        from bson.objectid import ObjectId
        try:
            return await self.index_cache.find_one({"_id": ObjectId(file_id_str)})
        except:
            return None
    
    async def delete_file(self, file_id):
         from bson.objectid import ObjectId
         await self.index_cache.delete_one({"_id": ObjectId(file_id)})
         
    async def clear_index(self):
        await self.index_cache.delete_many({})

    # --- USERS ---
    async def add_user(self, user_id, first_name, username):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {
                "first_name": first_name,
                "username": username,
                "joined_at": time.time()
             }},
            upsert=True
        )
        
    async def is_user_exist(self, user_id):
        return await self.users.find_one({"user_id": user_id})

    async def get_total_users(self):
        return await self.users.count_documents({})

    # --- TRENDING ---
    async def increase_view(self, anime_name):
        await self.trending.update_one(
            {"anime_name": anime_name},
            {"$inc": {"view_count": 1}},
            upsert=True
        )

    async def get_trending(self, limit=10):
        cursor = self.trending.find().sort("view_count", -1).limit(limit)
        return await cursor.to_list(length=limit)

    # --- FAVORITES ---
    async def add_favorite(self, user_id, anime_name):
        await self.favorites.update_one(
            {"user_id": user_id, "anime_name": anime_name},
            {"$set": {"added_at": time.time()}},
            upsert=True
        )

    async def remove_favorite(self, user_id, anime_name):
        await self.favorites.delete_one({"user_id": user_id, "anime_name": anime_name})

    async def get_favorites(self, user_id):
        cursor = self.favorites.find({"user_id": user_id})
        return await cursor.to_list(length=None)

    async def is_favorite(self, user_id, anime_name):
        return await self.favorites.find_one({"user_id": user_id, "anime_name": anime_name})

    # --- SETTINGS & ADS ---
    async def get_setting(self, key, default=None):
        doc = await self.settings.find_one({"key": key})
        return doc["value"] if doc else default

    async def set_setting(self, key, value):
        await self.settings.update_one(
            {"key": key},
            {"$set": {"value": value}},
            upsert=True
        )

    async def check_ad_cooldown(self, user_id, cooldown_seconds=3600):
        doc = await self.ads_cooldown.find_one({"user_id": user_id})
        current_time = time.time()
        if not doc:
            return True # Show ad
        if current_time - doc["last_ad_time"] > cooldown_seconds:
            return True
        return False

    async def update_ad_time(self, user_id):
        await self.ads_cooldown.update_one(
            {"user_id": user_id},
            {"$set": {"last_ad_time": time.time()}},
            upsert=True
        )

db = Database()
