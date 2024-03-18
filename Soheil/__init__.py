from asyncio import get_event_loop, new_event_loop, set_event_loop

from Soheil.logs import LOGGER
from Soheil.config import EA_LOGIN_PATH, DRIVER, TELE_CLIENT, config
from Soheil.database import check_mongo_uri

DRIVER.get(EA_LOGIN_PATH)

LOGGER(__name__).info("setting up event loop....")
try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

LOGGER(__name__).info("Starting Soheil Crawler...")
LOGGER(__name__).info("checking MongoDb URI....")
loop.run_until_complete(check_mongo_uri(config.MONGO_URI))
LOGGER(__name__).info("Starting TeleClient")


# TELETHON SETTINGS
TELE_CLIENT.start()
