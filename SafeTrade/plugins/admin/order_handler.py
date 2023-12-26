import uuid
from SafeTrade.helpers.start_constants import *
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from SafeTrade.database.MongoDB import saveAdminOrder
from SafeTrade.database.MongoDB import MongoDb as db


SAVED_ORDER = [
    [
        InlineKeyboardButton("فعال کردن", callback_data="ACTIVATE_ORDER"),
        InlineKeyboardButton("BACK TO MENU", callback_data="BACK_TO_ORDER"),
    ],
]

ORDER_EXISTS = [
    [
        InlineKeyboardButton("فعال کردن", callback_data="ACTIVATE_ORDER"),
        InlineKeyboardButton("BACK TO MENU", callback_data="BACK_TO_ORDER"),
    ]
]


async def orderHandler(text, message: Message, message_id):
    try:
        amount = int(text)
    except ValueError:
        return await message.reply_text(
            INVALID_TYPE, quote=True, reply_to_message_id=message_id
        )
    active_order = await db.admin_order.get_document_by_kwargs(status="P")
    if active_order is not None:
        return await message.reply_text(
            ACTIVE_ORDER_EXISTS,
            reply_markup=InlineKeyboardMarkup(ORDER_EXISTS),
            quote=True,
        )

    await saveAdminOrder(id=str(uuid.uuid4()), amount=amount)
    return await message.reply_text(
        ORDER_SAVED, reply_markup=InlineKeyboardMarkup(SAVED_ORDER), quote=True
    )
