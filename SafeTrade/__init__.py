import sys
import time

from asyncio import get_event_loop, new_event_loop, set_event_loop
import uvloop

from pyrogram.client import Client
from SafeTrade import config
from SafeTrade.database.Redis.Redis import check_redis_url
from SafeTrade.logs import LOGGER
from SafeTrade.database.MongoDB import check_mongo_uri
from SafeTrade.database.Redis import OrderHandler

uvloop.install()
LOGGER(__name__).info("Starting SafeTrade Bot...")
BotStartTime = time.time()

if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    LOGGER(__name__).critical(
        """
        =============================================================
        You MUST need to be on python 3.7 or above, shutting down the bot...
        =============================================================
        """
    )
    sys.exit(1)

LOGGER(__name__).info("setting up event loop....")
try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

LOGGER(__name__).info(
    r"""
   _____       ____   ______               __   
  / ___/____ _/ _____/_  ___________ _____/ ___ 
  \__ \/ __ `/ /_/ _ \/ / / ___/ __ `/ __  / _ \
 ___/ / /_/ / __/  __/ / / /  / /_/ / /_/ /  __/
/____/\__,_/_/  \___/_/ /_/   \__,_/\__,_/\___/ 

"""
)
LOGGER(__name__).info("initiating the client....")
LOGGER(__name__).info("checking MongoDb URI....")
loop.run_until_complete(check_mongo_uri(config.MONGO_URI))
LOGGER(__name__).info("checkoung Redis URI")
loop.run_until_complete(check_redis_url(config.REDIS_URL, config.REDIS_PORT))


plugins = dict(root="SafeTrade/plugins")
bot = Client(
    "SafeTrade",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=plugins,
)
