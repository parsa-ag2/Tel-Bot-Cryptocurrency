import os
from dotenv import load_dotenv

load_dotenv()


# =====================
# Telegram
# =====================

BOT_TOKEN = os.getenv("BOT_TOKEN")

GROUP_INVITE_LINK = os.getenv("GROUP_INVITE_LINK")

CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")


# =====================
# Twelve Data API
# =====================

TWELVE_DATA_API_KEY = os.getenv(
    "TWELVE_DATA_API_KEY"
)

TWELVE_DATA_BASE_URL = (
    "https://api.twelvedata.com"
)

# =====================
# Database
# =====================

DB_HOST = os.getenv("DB_HOST", "localhost")

DB_PORT = int(os.getenv("DB_PORT", 3306))

DB_NAME = os.getenv("DB_NAME")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")


# =====================
# Owner
# =====================

OWNER_ID = int(os.getenv("OWNER_ID"))