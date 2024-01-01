import redis
import time
import asyncio
from telethon import TelegramClient, types
import json
from Soheil.core import redis_listener

# is_active = True
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [redis_listener()]
    try:
        # Gather and run the tasks concurrently
        loop.run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to gracefully shutdown
        print("KeyboardInterrupt: Cancelling tasks...")
