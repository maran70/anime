import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    
    # Bot Tokens
    INDEX_BOT_TOKEN = os.getenv("INDEX_BOT_TOKEN", "")
    FILE_BOT_TOKEN = os.getenv("FILE_BOT_TOKEN", "")
    FILE_BOT_USERNAME = os.getenv("FILE_BOT_USERNAME", "FileDeliveryBot")

    
    # Database
    MONGO_URI = os.getenv("MONGO_URI", "")
    DB_NAME = os.getenv("DB_NAME", "anime_bot_db")
    
    # Channels & Admins
    DB_CHANNEL_ID = int(os.getenv("DB_CHANNEL_ID", "0")) # Private Channel ID
    # Support ADMINS or ADMIN_IDS
    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", os.getenv("ADMINS", "")).split()]
    
    # Force Join
    FORCE_JOIN_CHANNEL_ID = int(os.getenv("FORCE_JOIN_CHANNEL_ID", "0"))
    FORCE_JOIN_CHANNEL_LINK = os.getenv("FORCE_JOIN_CHANNEL_LINK", "")
    
    # Settings
    NEW_EPISODE_HIGHLIGHT_HOURS = 24
    CAPTION_MODE = int(os.getenv("CAPTION_MODE", "2")) # 1=Original, 2=Clean, 3=No Caption
