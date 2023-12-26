import uuid
from pyrogram.types import Message, InlineKeyboardButton

from SafeTrade.helpers.start_constants import *
from SafeTrade.database.MongoDB import saveOrder, saveOrderItem
from SafeTrade.database.MongoDB import MongoDb as db
from SafeTrade.database.Redis import OrderHandler

ORDER_OPTIONS = [
    [
        InlineKeyboardButton("ادامه فروش", callback_data="CONTINUE_TRADE"),
        InlineKeyboardButton("اتمام فروش", callback_data="FINISH_TRADE"),
    ],
]


async def tradeHandler(
    text, message: Message, message_id, order_id, user_id, handler: OrderHandler
):
    """
    setup and order for a user
    text: contains supply amount
    order_id: user order that contains order_items
    user_id: user id that trying to sell coins
    handler: OrderHandler object to publish data to Soheil(the crawler) service
    """
    try:
        amount = int(text)
    except ValueError:
        await message.reply_text(
            INVALID_TYPE, quote=True, reply_to_message_id=message_id
        )

    order_item = await db.order_item.get_document_by_kwargs(
        is_listed=False, order_id=order_id, has_bought=False
    )

    if order_item is not None:
        return await message.reply_text(
            "YOU ALREADE HAVE ORDER ITEM IN PROGRESS",
            reply_to_message_id=message_id,
        )

    # initiate and order item
    try:
        await saveOrderItem(str(uuid.uuid4()), order_id, supply=amount)
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
        # TODO: should apply logger
        print(f"Error: {e}")
