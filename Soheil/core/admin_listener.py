import time
import redis
import json
from Soheil.config import REDIS_ADMIN_CHANNEL, CLIENT
from asyncio import get_event_loop, new_event_loop, set_event_loop
from Soheil.functions import update_telegram_message
from Soheil.core.login_account import login_account


pubsub_admin = CLIENT.pubsub()
pubsub_admin.subscribe(REDIS_ADMIN_CHANNEL)


async def listen_for_admin_order():
    for message in pubsub_admin.listen():
        if message["type"] == "message":
            await login_account(message["data"])
