import time
import redis
import json
from Soheil.config import REDIS_ADMIN_CHANNEL, REDIS_HOST, REDIS_PORT, CLIENT
from asyncio import get_event_loop, new_event_loop, set_event_loop
from Soheil.functions import update_telegram_message


pubsub_admin = CLIENT.pubsub()
pubsub_admin.subscribe(REDIS_ADMIN_CHANNEL)


async def listen_for_admin_order():
    for message in pubsub_admin.listen():
        if message["type"] == "message":
            print("proccessing")
