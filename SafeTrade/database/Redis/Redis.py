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
        self.admin_key = f"admin:{user_id}"
        self.redis_client = redis.StrictRedis(
            host=REDIS_URL, port=REDIS_PORT, decode_responses=True
        )

    async def set_order(self, data):
        """
        setup an order for a user
        {
            "order_id": str,
            "admin_order_id": str,
            "is_active": bool,
        }
        """

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

    async def set_admin(self, data=None):
        """
        setup admin access control
        """
        if data is None:
            data = {
                "can_setup_order": False,
            }

        serialized_data = json.dumps(data)

        self.redis_client.set(self.admin_key, serialized_data)

    async def get_admin(self):
        """
        get admin access control settings
        """
        data = self.redis_client.get(self.admin_key)
        if data is None:
            return None
        return json.loads(data)

    async def active_admin_setup_order(self):
        """
        active admin access control to send messages
        """
        data = await self.get_admin()
        data["can_setup_order"] = True
        await self.set_admin(data)

    async def deactive_admin_setup_order(self):
        """
        active admin access control to send messages
        """
        data = await self.get_admin()
        data["can_setup_order"] = False
        await self.set_admin(data)


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
