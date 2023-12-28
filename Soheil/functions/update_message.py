import types
from Soheil.config import TELE_CLIENT
from telethon import types
from Soheil.helpers import BOUGHT_CARD


# Function to update a Telegram message
async def update_telegram_message(chat_id, message_id, new_text):
    try:
        bought = types.KeyboardButtonCallback(BOUGHT_CARD, data="DONE_TRADE")
        # Create a row with the button
        row = [bought]

        await TELE_CLIENT.edit_message(
            chat_id,
            message_id,
            new_text,
            buttons=row,
        )

    except Exception as e:
        print(f"Error updating message: {e}")
