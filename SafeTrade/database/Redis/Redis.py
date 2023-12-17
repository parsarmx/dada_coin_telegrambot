from sys import exit as exiter
from SafeTrade.logging import LOGGER
from SafeTrade.config import REDIS_CACHE_TTL, REDIS_PORT, REDIS_URL

import redis
import json


class OrderHandler:
    def __init__(self, user_id):
        self.user_id = user_id
        self.redis_client = redis.StrictRedis(
            host=REDIS_URL, port=REDIS_PORT, decode_responses=True
        )

    async def set_order(self, data: dict):
        """
        setup an order for a user
        """
        key = f"order:{self.user_id}"
        serialized_data = json.dumps(data)

        self.redis_client.set(key, serialized_data)
        self.redis_client.expire(key, REDIS_CACHE_TTL)

    async def get_order(self):
        key = f"order:{self.user_id}"
        print(self.redis_client.get(key))


async def check_redis_url(url: str, port: int) -> None:
    try:
        redis_client = redis.StrictRedis(
            host=url,
            port=port,
            decode_responses=True,
        )

        redis_client.client_id()
    except:
        LOGGER(__name__).error(  # type: ignore
            "Error in Establishing connection with Redis URL. Please enter valid url in the config section."
        )
        exiter(1)
