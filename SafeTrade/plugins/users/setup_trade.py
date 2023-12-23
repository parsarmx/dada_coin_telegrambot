import uuid
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
)

from SafeTrade.helpers.start_constants import *
from SafeTrade.database.MongoDB import saveOrder, saveOrderItem
from SafeTrade.database.MongoDB import MongoDb as db
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
    # TODO: THIS FUNCTION SHOULD SEND MESSAGES TO WANTED FUNCTIONS NOT WORKING ALONE
    # textMessageHandler maybe

    user_id = message.from_user.id
    handler = OrderHandler(user_id)
    orders = await handler.get_order()
    message_id = message.id

    # check if user has active order
    if orders is None or not orders.get("is_active"):
        return await message.reply_text(INVALID_MESSAGE, quote=True)

    text = message.text

    # check if sent message type is correct
    try:
        int(text)
    except ValueError:
        return await message.reply_text(
            INVALID_TYPE, quote=True, reply_to_message_id=message_id
        )

    await saveOrder(
        order_id=orders.get("order_id"),
        user_id=user_id,
    )

    order_item = await db.order_item.get_document_by_kwargs(
        is_listed=False, order_id=orders.get("order_id")
    )
    print(order_item)

    if order_item is not None:
        return await message.reply_text(
            "YOU ALREADE HAVE ORDER ITEM IN PROGRESS",
            reply_to_message_id=message_id,
        )
    # initiate an order
    try:
        await saveOrderItem(str(uuid.uuid4()), orders.get("order_id"), supply=text)
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

        await handler.publish_update(data)

    except Exception as e:
        # should apply logger
        print(f"Error: {e}")
