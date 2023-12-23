from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from SafeTrade.database.MongoDB import MongoDb as db
from SafeTrade.database.MongoDB import saveOrder

from SafeTrade.helpers.start_constants import *
from SafeTrade.helpers.decorator import rate_limiter
from SafeTrade.database.Redis import OrderHandler

FINALIZE_TRADE = [
    [
        InlineKeyboardButton("دریافت رسید", callback_data="GET_RECEIPT"),
    ],
]


@Client.on_callback_query(filters.regex("_TRADE"))  # type: ignore
@rate_limiter
async def tradeCallbacks(client, CallbackQuery: CallbackQuery):
    clicker_user_id = CallbackQuery.from_user.id
    user_id = CallbackQuery.message.reply_to_message.from_user.id

    if clicker_user_id != user_id:
        return await CallbackQuery.answer("This command is not initiated by you.")

    chat_id = CallbackQuery.message.chat.id
    message_id = CallbackQuery.message.id

    if CallbackQuery.data == "START_TRADE":
        handler = OrderHandler(user_id)
        # user orders are ready to process
        order = await handler.get_order()

        # activate order status to let user set orders
        if order != None and not order.get("is_active"):
            await handler.active_order()
        else:
            await handler.set_order()

        await CallbackQuery.edit_message_text(
            START_TRADE_CAPTION,
        )

    elif CallbackQuery.data == "CONTINUE_TRADE":
        try:
            # Delete the last message sent by the bot
            await client.delete_messages(chat_id, message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

    elif CallbackQuery.data == "FINISH_TRADE":
        await CallbackQuery.edit_message_text(
            FINISH_TRADE,
            reply_markup=InlineKeyboardMarkup(FINALIZE_TRADE),
        )
