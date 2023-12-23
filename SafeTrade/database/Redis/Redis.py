from sys import exit as exiter
from SafeTrade.logging import LOGGER
from SafeTrade.config import (
    REDIS_PORT,
    REDIS_URL,
    REDIS_ORDERS_CHANNEL,
)
from typing import List, Dict, Any
import redis
import json
import uuid


class OrderHandler:
    def __init__(self, user_id):
        self.order_key = f"order:{user_id}"
        self.redis_client = redis.StrictRedis(
            host=REDIS_URL, port=REDIS_PORT, decode_responses=True
        )

    async def set_order(self, data=None):
        """
        setup an order for a user
        """

        if data is None:
            data = {
                "order_id": str(uuid.uuid4()),
                "is_active": True,
            }

        serialized_data = json.dumps(data)

        self.redis_client.set(self.order_key, serialized_data)

    async def get_order(self) -> List[Dict[str, Any]]:
        """
        get user orders
        """
        data = self.redis_client.get(self.order_key)

        if data is None:
            return None
        return json.loads(data)

    async def deactive_order(self):
        """
        deactive order temporary
        """
        data = await self.get_order()
        data["is_active"] = False
        await self.set_order(data)

    async def active_order(self):
        """
        active order temporary
        """
        data = await self.get_order()
        data["is_active"] = True
        await self.set_order(data)

    async def delete_order(self):
        self.redis_client.delete(self.order_key)

    async def publish_update(self, message: dict):
        """
        Publish a message about an order update to the pubsub channel
        """
        self.redis_client.publish(REDIS_ORDERS_CHANNEL, json.dumps(message))


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
