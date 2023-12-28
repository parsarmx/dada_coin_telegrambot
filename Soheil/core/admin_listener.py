import time
import redis
import json
from Soheil.config import REDIS_ORDER_CHANNEL, REDIS_HOST, REDIS_PORT, CLIENT
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
    for message in pubsub_order.listen():
        if message["type"] == "message":
            print("proccessing...")
            time.sleep(5)

            print(message["data"])
            data = json.loads(message["data"])

            await update_telegram_message(
                data.get("chat_id"),
                data.get("message_id"),
                "بازیکن با موفقیت لیست شد.\nلطفا بعد از خرید دکمه خریدم رو بزنید.",
            )
