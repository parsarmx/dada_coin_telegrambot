import json
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pyrogram.enums.parse_mode import ParseMode

from SafeTrade.database.MongoDB import MongoDb as db
from pyrogram.types import Message, InlineKeyboardButton
from SafeTrade.config import REDIS_ADMIN_CHANNEL

from SafeTrade.helpers.start_constants import *
from SafeTrade.database.MongoDB import saveAdminOrder
from SafeTrade.helpers.decorator import rate_limiter
from SafeTrade.database.Redis import OrderHandler

ADMIN_BUTTON = [
    [
        InlineKeyboardButton("ثبت سفارش جدید", callback_data="NEW_ORDER"),
        InlineKeyboardButton("وضعیت سفارش ها", callback_data="STATUS_ORDER"),
    ],
]

FAILED_ACTIVATION_BUTTON = [
    [
        InlineKeyboardButton("BACK", callback_data="BACK_TO_ORDER"),
    ]
]

ACTIVATION_SUCCEFULL_BUTTON = [
    [
        InlineKeyboardButton("BACK", callback_data="BACK_TO_ORDER"),
        InlineKeyboardButton("وضعیت سفارش", callback_data="STATUS_ORDER"),
    ]
]


@Client.on_callback_query(filters.regex("_ORDER"))
@rate_limiter
async def adminCallbscks(_, CallbackQuery: CallbackQuery):
    clicker_user_id = CallbackQuery.from_user.id
    user_id = CallbackQuery.message.reply_to_message.from_user.id
    handler = OrderHandler(user_id=user_id)

    if clicker_user_id != user_id:
        return await CallbackQuery.answer("This command is not initiated by you.")

    if CallbackQuery.data == "NEW_ORDER":
        # set admin access to send messages
        await handler.active_admin_setup_order()
        await CallbackQuery.edit_message_text(
            SETUP_ADMIN_ORDER, parse_mode=ParseMode.HTML
        )

    elif CallbackQuery.data == "BACK_TO_ORDER":
        await handler.deactive_admin_setup_order()
        await CallbackQuery.edit_message_text(
            ADMIN_PANEL, reply_markup=InlineKeyboardMarkup(ADMIN_BUTTON)
        )

    elif CallbackQuery.data == f"ACTIVATE_ORDER":
        await handler.deactive_admin_setup_order()
        active_order = await db.admin_order.get_document_by_kwargs(is_active=False)
        if active_order is None:
            return await CallbackQuery.edit_message_text(
                FAILED_ACTIVATION,
                reply_markup=InlineKeyboardMarkup(FAILED_ACTIVATION_BUTTON),
            )
        await saveAdminOrder(
            id=active_order.get("_id"),
            amount=active_order.get("amount"),
            email=active_order.get("email"),
            password=active_order.get("password"),
            backup_code=active_order.get("backup_code"),
            is_active=True,
            status="P",
        )

        # delete this keys because json cant serializer them
        del active_order["created_at"]
        del active_order["updated_at"]

        print(active_order)
        await handler.publish_update(
            active_order,
            REDIS_ADMIN_CHANNEL,
        )

        await CallbackQuery.edit_message_text(
            ACTIVATION_SUCCEFULL,
            reply_markup=InlineKeyboardMarkup(FAILED_ACTIVATION_BUTTON),
        )
