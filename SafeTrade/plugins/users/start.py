from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from SafeTrade import bot
from SafeTrade.database.MongoDB import MongoDb
from SafeTrade.database.Redis import OrderHandler
from SafeTrade.database.MongoDB.database import saveUser
from SafeTrade.helpers.start_constants import *
from SafeTrade.helpers.decorator import rate_limiter
from SafeTrade.config import OWNER_USERID, ADMIN_USERID

START_BUTTON = [
    [
        InlineKeyboardButton("📖 فروش", callback_data="TRADE_BUTTON"),
        InlineKeyboardButton("👨‍💻 نحوه استفاده", callback_data="ABOUT_BUTTON"),
    ],
]


TRADE_BUTTON = [
    [InlineKeyboardButton("انتخاب سفارش", callback_data="START_TRADE")],
    [
        InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON"),
    ],
]

GOBACK_1_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")]]
# GOBACK_2_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="TRADE_BUTTON")]]


@Client.on_message(filters.command(["start", "help"]))
@rate_limiter
async def start(_, message: Message):
    await saveUser(message.from_user)
    handler = OrderHandler(message.from_user.id)
    orders = await handler.get_order()

    # makes sure user cant set order
    if orders != None and orders.get("is_active"):
        await handler.deactive_order()

    return await message.reply_text(
        START_CAPTION, reply_markup=InlineKeyboardMarkup(START_BUTTON), quote=True
    )


@Client.on_callback_query(filters.regex("_BUTTON"))
@rate_limiter
async def botCallbacks(_, CallbackQuery: CallbackQuery):
    clicker_user_id = CallbackQuery.from_user.id
    user_id = CallbackQuery.message.reply_to_message.from_user.id

    if clicker_user_id != user_id:
        return await CallbackQuery.answer("This command is not initiated by you.")

    if CallbackQuery.data == "ABOUT_BUTTON":
        await CallbackQuery.edit_message_text(
            ABOUT_CAPTION, reply_markup=InlineKeyboardMarkup(GOBACK_1_BUTTON)
        )

    elif CallbackQuery.data == "TRADE_BUTTON":
        await CallbackQuery.edit_message_text(
            TRADE_CAPTION, reply_markup=InlineKeyboardMarkup(TRADE_BUTTON)
        )

    elif CallbackQuery.data == "START_BUTTON":
        await CallbackQuery.edit_message_text(
            START_CAPTION, reply_markup=InlineKeyboardMarkup(START_BUTTON)
        )

    await CallbackQuery.answer()
