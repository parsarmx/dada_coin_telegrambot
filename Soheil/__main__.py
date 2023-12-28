import redis
import time
import asyncio
from telethon import TelegramClient, types
import json
from Soheil.core import listen_for_admin_order, listen_for_order_item

# is_active = True
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [listen_for_admin_order(), listen_for_order_item()]
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
