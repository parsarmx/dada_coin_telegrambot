from selenium import webdriver
from os import getenv
from dotenv import load_dotenv
from telethon import TelegramClient
import redis

load_dotenv("Soheil/.env")

# EA_URLS
EA_LOGIN_PATH = getenv("EA_LOGIN_PATH")

# CRAWLER CONFIGS
DRIVER = webdriver.Chrome()

# REDIS
REDIS_ORDER_CHANNEL = getenv("REDIS_ORDER_CHANNEL")
REDIS_ADMIN_CHANNEL = getenv("REDIS_ADMIN_CHANNEL")
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_PASSWORD = getenv("REDIS_PASSWOR")

# TELETON CONFIG
BOT_TOKEN = getenv("BOT_TOKEN")
API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
TELE_CLIENT = TelegramClient(
    BOT_TOKEN,
    API_ID,
    API_HASH,
)

# REDIS SETTINGS
CLIENT = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)
