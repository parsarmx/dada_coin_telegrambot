import uuid
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    Message,
)
from SafeTrade.helpers.start_constants import *
from SafeTrade.database.MongoDB import MongoDb as db
from SafeTrade.helpers.decorator import rate_limiter
from SafeTrade.database.Redis import OrderHandler
from SafeTrade.plugins.admin.order_handler import orderHandler
from SafeTrade.plugins.users.trade_handler import tradeHandler


@Client.on_message(filters.text & ~filters.command(["start", "help", "admin"]))
@rate_limiter
async def adminMessageHandler(_, message: Message):
    user_id = message.from_user.id
    handler = OrderHandler(user_id=user_id)
    admin_access = await handler.get_admin()
    user_orders = await handler.get_order()
    message_id = message.id
    if admin_access is not None and admin_access.get("can_setup_order"):
        text = message.text
        await orderHandler(text, message, message_id)
    # check if user has active order
    if user_orders is not None and user_orders.get("is_active"):
        text = message.text
        await tradeHandler(
            text,
            message,
            message.id,
            user_orders.get("order_id"),
            user_id,
            handler,
        )
