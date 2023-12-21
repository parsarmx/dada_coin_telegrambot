import uuid
import json
import time
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from SafeTrade.helpers.start_constants import *
from SafeTrade.helpers.decorator import rate_limiter
from SafeTrade.database.Redis import OrderHandler


ORDER_OPTIONS = [
    [
        InlineKeyboardButton("ادامه فروش", callback_data="CONTINUE_TRADE"),
        InlineKeyboardButton("اتمام فروش", callback_data="FINISH_TRADE"),
    ],
]


@Client.on_message(filters.text & ~filters.command(["start", "help"]))
@rate_limiter
async def setUpTradeOrder(_, message: Message):
    user_id = message.from_user.id
    order_handler = OrderHandler(user_id)
    orders = await order_handler.get_order()
    message_id = message.id

    # check if user has active order
    if orders is None:
        return await message.reply_text(INVALID_MESSAGE, quote=True)

    text = message.text

    # check if sent message type is correct
    try:
        int(text)
    except ValueError:
        return await message.reply_text(
            INVALID_TYPE, quote=True, reply_to_message_id=message_id
        )

    # initiate an order
    try:
        progress_message = await message.reply_text(
            TRADE_IN_PROGRESS, reply_to_message_id=message_id
        )

        data = {
            "id": str(uuid.uuid4()),
            "amount": text,
            "is_done": False,
            "chat_id": message.chat.id,
            "message_id": progress_message.id,
            "user_id": user_id,
        }

        orders.append(data)

        await order_handler.publish_update(data)

    except Exception as e:
        # should apply logger
        print(f"Error: {e}")
