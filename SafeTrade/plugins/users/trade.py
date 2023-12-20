import uuid
import time
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from SafeTrade.helpers.start_constants import *
from SafeTrade.helpers.decorator import rate_limiter
from SafeTrade.database.Redis import OrderHandler

SETUP_ORDER = [
    [
        InlineKeyboardButton("📖 ادامه فروش", callback_data="CONTINUE"),
        InlineKeyboardButton("👨‍💻 ااتمام فروش", callback_data="DONE"),
    ],
]


@Client.on_callback_query(filters.regex("_TRADE"))  # type: ignore
@rate_limiter
async def tradeCallbacks(_, CallbackQuery: CallbackQuery):
    clicker_user_id = CallbackQuery.from_user.id
    user_id = CallbackQuery.message.reply_to_message.from_user.id

    if clicker_user_id != user_id:
        return await CallbackQuery.answer("This command is not initiated by you.")

    if CallbackQuery.data == "START_TRADE":
        order = OrderHandler(user_id)

        # user orders are ready to process
        await order.set_order()
        await CallbackQuery.edit_message_text(
            START_TRADE_CAPTION,
        )


@Client.on_callback_query(filters.regex("CONTINUE"))
async def continueOrder(client, CallbackQuery: CallbackQuery):
    chat_id = CallbackQuery.message.chat.id
    message_id = CallbackQuery.message.id
    try:
        # Delete the last message sent by the bot
        await client.delete_messages(chat_id, message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")


@Client.on_message(filters.text)
async def setUpTradeOrder(_, message: Message):
    user_id = message.from_user.id
    order_handler = OrderHandler(user_id)
    orders = await order_handler.get_order()
    # check if user has active order
    if orders is None:
        return await message.reply_text(INVALID_MESSAGE, quote=True)
    text = message.text

    # check if sent message type is correct
    try:
        int(text)
    except ValueError:
        return await message.reply_text(INVALID_TYPE, quote=True)

    # initiate an order
    data = {
        "id": str(uuid.uuid4()),
        "amount": text,
        "is_done": False,
    }

    orders.append(data)
    await order_handler.set_order(orders)
    try:
        progress_message = await message.reply_text(TRADE_IN_PROGRESS)
        time.sleep(5)

        await progress_message.edit_caption(
            CARD_HAS_BEEN_LISTED,
            reply_markup=InlineKeyboardMarkup(SETUP_ORDER),
        )
    except Exception as e:
        print(f"Error: {e}")
