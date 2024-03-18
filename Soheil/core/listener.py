from Soheil.config import CLIENT, REDIS_ADMIN_CHANNEL, REDIS_ORDER_CHANNEL
from Soheil.core.is_amount_valid import is_amount_valid
from Soheil.core.login_account import login_account

pubsub = CLIENT.pubsub()
pubsub.subscribe(REDIS_ADMIN_CHANNEL, REDIS_ORDER_CHANNEL)


async def redis_listener():
    for message in pubsub.listen():
        if message.get("type") == "message":
            if message.get("channel") == REDIS_ADMIN_CHANNEL:
                is_logged_in = await login_account(message.get("data"))
            elif message.get("channel") == REDIS_ORDER_CHANNEL:
                amount_valid = await is_amount_valid(
                    message.get("admin_order_id"), message.get("amount")
                )
                print(amount_valid)
