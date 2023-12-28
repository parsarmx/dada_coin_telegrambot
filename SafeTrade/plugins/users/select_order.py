import uuid
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from SafeTrade.database.MongoDB import MongoDb as db
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
)

from SafeTrade.helpers.start_constants import *
from SafeTrade.database.MongoDB import saveOrder
from SafeTrade.helpers.decorator import rate_limiter
from SafeTrade.database.Redis import OrderHandler


@Client.on_callback_query(filters.regex(":SELECT"))
@rate_limiter
async def selectOrderCallbacks(_, CallbackQuery: CallbackQuery):
    clicker_user_id = CallbackQuery.from_user.id
    user_id = CallbackQuery.message.reply_to_message.from_user.id
    handler = OrderHandler(user_id=user_id)
    # user orders are ready to process
    cached_order = await handler.get_order()

    if clicker_user_id != user_id:
        return await CallbackQuery.answer("This command is not initiated by you.")

    admin_order_id, _ = CallbackQuery.data.split(":")
    user_order = await db.orders.get_document_by_kwargs(status="P")

    # check if user order is already is in redis
    if (
        cached_order != None
        and user_order != None
        and not cached_order.get("is_active")
    ):
        await handler.active_order()

    # if its not in redis check if user has any active order for this admin_order
    elif cached_order == None and user_order != None:
        if admin_order_id == user_order.get("admin_order_id"):
            data = {
                "order_id": user_order.get("_id"),
                "admin_order_id": admin_order_id,
                "is_active": True,
            }
            await handler.set_order(data)

    # if the user dosent have any active order for an admin_order create a new order
    else:
        order_id = str(uuid.uuid4())
        data = {
            "order_id": order_id,
            "admin_order_id": admin_order_id,
            "is_active": True,
        }

        await saveOrder(order_id, user_id, admin_order_id)
        await handler.set_order(data)

    await CallbackQuery.edit_message_text(SETUP_ADMIN_ORDER)
