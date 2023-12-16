from SafeTrade.database.MongoDB import MongoDb as db
from datetime import datetime, timezone


async def saveUser(user):
    """
    Save the new user id in the database if it is not already there.
    """

    insert_format = {
        "first_name": (user.first_name or " "),
        "last_name": (user.last_name or ""),
        "username": user.username,
        "date": datetime.now(timezone.utc),
    }
    await db.users.update_document(user.id, insert_format)


# async def saveChat(chatid):
#     """
#     Save the new chat id in the database if it is not already there.
#     """

#     insert_format = {"date": datetime.now(timezone.utc)}
#     await db.chats.update_document(chatid, insert_format)
