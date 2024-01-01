from Soheil.config import CLIENT, REDIS_ADMIN_CHANNEL, REDIS_ORDER_CHANNEL
from Soheil.core.login_account import login_account

pubsub = CLIENT.pubsub()
pubsub.subscribe(REDIS_ADMIN_CHANNEL, REDIS_ORDER_CHANNEL)


async def redis_listener():
    for message in pubsub.listen():
        print(message)
        if message.get("type") == "message":
            if message.get("channel") == REDIS_ADMIN_CHANNEL:
                is_logged_in = await login_account(message.get("data"))
                print(is_logged_in)
            elif message.get("channel") == REDIS_ORDER_CHANNEL:
                pass
