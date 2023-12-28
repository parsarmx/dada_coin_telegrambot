import json
from os import getenv
from dotenv import load_dotenv

load_dotenv("SafeTrade/.env")

API_ID = int(getenv("API_ID"))  # type: ignore
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_USERID = json.loads(getenv("OWNER_USERID"))  # type: ignore
ADMIN_USERID = OWNER_USERID
try:
    ADMIN_USERID += json.loads(getenv("ADMIN_USERID"))  # type: ignore
except:
    pass
ADMIN_USERID = list(set(ADMIN_USERID))

### MONGO
MONGO_URI = getenv("MONGO_URI")

### REDIS
REDIS_URL: str = getenv("REDIS_URL")  # type: ignore
REDIS_PORT = int(getenv("REDIS_PORT"))  # type: ignore
REDIS_PASSWORD = getenv("REDIS_PASSWORD")
REDIS_CACHE_TTL = int(getenv("REDIS_CACHE_TTL"))  # type: ignore
REDIS_ORDERS_CHANNEL = getenv("REDIS_ORDERS_CHANNEL")
