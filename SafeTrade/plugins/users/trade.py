from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


from SafeTrade.database.MongoDB import MongoDb as db
from SafeTrade.database.Redis import OrderHandler
from SafeTrade.helpers.start_constants import *
from SafeTrade.helpers.decorator import rate_limiter

FINALIZE_TRADE = [
    [
        InlineKeyboardButton("دریافت رسید", callback_data="GET_RECEIPT"),
    ],
]

DONE_TRADE = [
    [
        InlineKeyboardButton("ادامه خرید", callback_data="CONTINUE_TRADE"),
        InlineKeyboardButton("پایان فروش", callback_data="FINISH_TRADE"),
    ],
]

NO_ACTIVE_ORDER = [
    [
        InlineKeyboardButton("BACK", callback_data="START_BUTTON"),
    ]
]

BOUGHT_CARD = [
    [
        InlineKeyboardButton("خریدم", callback_data="DONE_TRADE"),
    ]
]


# TODO:this function create one order for now
# should change later
async def orderButtons():
    order = await db.admin_order.get_document_by_kwargs(status="P")
    return [
        InlineKeyboardButton(
            f"{order.get('amount'):,} - {order.get('status')}",
            callback_data=f"{order.get('_id')}:SELECT",
        )
    ]


BACK_BUTTON = [
    InlineKeyboardButton("BACK", callback_data="START_BUTTON"),
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
    handler = OrderHandler(user_id=user_id)

    if CallbackQuery.data == "START_TRADE":
        admin_order = await db.admin_order.get_document_by_kwargs(status="P")
        # activate order status to let user set orders
        if admin_order is None:
            return await CallbackQuery.edit_message_text(
                NO_ACTIVE_ORDER_AVAILABLE,
                reply_markup=InlineKeyboardMarkup(NO_ACTIVE_ORDER),
            )
        buttons = await orderButtons()
        await CallbackQuery.edit_message_text(
            CHOOSE_AN_ORDER,
            reply_markup=InlineKeyboardMarkup([buttons, BACK_BUTTON]),
        )

    elif CallbackQuery.data == "DONE_TRADE":
        # TODO: should check if user has bought card successfully
        has_bought = True
        if not has_bought:
            return await CallbackQuery.edit_message_text(
                CARD_STILL_EXISTS,
                reply_markup=InlineKeyboardMarkup(BOUGHT_CARD),
            )
        user_order = handler.get_order()
        order_id = user_order.get("order_id")

        order_item = db.order_item.get_document_by_kwargs(
            order_id=order_id, is_listed=True, has_bought=False, is_verified=True
        )

        await CallbackQuery.edit_message_text(
            FINISH_TRADE,
            reply_markup=InlineKeyboardMarkup(DONE_TRADE),
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
