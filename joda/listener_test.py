import redis
import time
from telethon import TelegramClient, types
from pymongo import MongoClient
import json

from asyncio import get_event_loop, new_event_loop, set_event_loop

try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()


# Setup your Telegram client
tele_client = TelegramClient(
    "6674884315:AAGDLXqblYPwLVN8L9iR4MlaWjTNXsDuIik",
    "1485960",
    "30df8f9d74b48f998e22419f62950047",
)
tele_client.start()


client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
pubsub = client.pubsub()
pubsub.subscribe("orders.proccess")


# Function to update a Telegram message
async def update_telegram_message(chat_id, message_id, new_text):
    try:
        bought = types.KeyboardButtonCallback("خریدم!", data="DONE_TRADE")
        # Create a row with the button
        row = [bought]

        await tele_client.edit_message(
            chat_id,
            message_id,
            new_text,
            buttons=row,
        )

    except Exception as e:
        print(f"Error updating message: {e}")


is_active = True
while True:
    if is_active:
        for message in pubsub.listen():
            if message["type"] == "message":
                print("proccessing...")
                time.sleep(5)

                print(message["data"])
                data = json.loads(message["data"])

                MongoClient()
                loop.run_until_complete(
                    update_telegram_message(
                        data.get("chat_id"),
                        data.get("message_id"),
                        "بازیکن با موفقیت لیست شد.\nلطفا بعد از خرید دکمه خریدم رو بزنید.",
                    )
                )
