import redis

from Soheil.logs import LOGGER
from Soheil.config import EA_LOGIN_PATH, DRIVER, TELE_CLIENT

DRIVER.get(EA_LOGIN_PATH)

LOGGER(__name__).info("Starting Soheil Crawler...")
LOGGER(__name__).info("Starting TeleClient")

# TELETHON SETTINGS
TELE_CLIENT.start()
