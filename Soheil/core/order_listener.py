import time
import redis
import json
import asyncio
from Soheil.config import REDIS_ORDER_CHANNEL, CLIENT
from asyncio import get_event_loop, new_event_loop, set_event_loop
from Soheil.functions import update_telegram_message


pubsub_order = CLIENT.pubsub()
pubsub_order.subscribe(REDIS_ORDER_CHANNEL)


try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()


async def listen_for_order_item():
    try:
        while True:
            message = await pubsub_order.get_message()
            if message and message.get("type") == "message":
                print("Processing order item")
                # Process order item logic here...
                print("Processing order item completed")
    except asyncio.CancelledError:
        print("listen_for_order_item task cancelled")
