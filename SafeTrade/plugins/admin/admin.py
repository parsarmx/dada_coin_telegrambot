from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from SafeTrade.database.MongoDB import MongoDb
from SafeTrade.database.Redis import OrderHandler
from SafeTrade.helpers.start_constants import *
from SafeTrade.helpers.decorator import rate_limiter
from SafeTrade.config import ADMIN_USERID

ADMIN_BUTTON = [
    [
        InlineKeyboardButton("ثبت سفارش جدید", callback_data="NEW_ORDER"),
        InlineKeyboardButton("وضعیت سفارش ها", callback_data="STATUS_ORDER"),
    ],
]


@Client.on_message(filters.command(["admin"]))
@rate_limiter
async def admin(_, message: Message):
    user_id = message.from_user.id
    handler = OrderHandler(user_id=user_id)
    await handler.set_admin()
    if user_id not in ADMIN_USERID:
        return

    return await message.reply_text(
        ADMIN_PANEL, reply_markup=InlineKeyboardMarkup(ADMIN_BUTTON), quote=True
    )
