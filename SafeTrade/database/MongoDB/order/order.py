from SafeTrade.database.MongoDB import MongoDb as db
from datetime import datetime, timezone


async def saveOrder(order_id, user_id, status="P"):
    """
    Initiate an order for a user
    """
    allowed_statuses = ["P", "D", "C"]
    if status not in allowed_statuses:
        raise ValueError("Invalid order status")

    current_time = datetime.now(timezone.utc)
    existing_order = await db.orders.get_document_by_kwargs(
        _id=order_id,
        user_id=user_id,
        status="P",
    )

    # doing this because dont want to update created_at every time
    if existing_order:
        insert_format = {
            "updated_at": current_time,
        }
    else:
        insert_format = {
            "user_id": user_id,
            "status": status,
            "total_coins": 0,
            "created_at": current_time,
            "updated_at": current_time,
        }

    await db.orders.update_document(order_id, insert_format)


async def saveOrderItem(order_item_id, order_id, supply: int):
    """
    save orderItem for an order
    """

    current_time = datetime.now(timezone.utc)

    insert_format = {
        "order_id": order_id,
        "sypply": supply,
        "card_amount": None,
        "buy_price": None,
        "sell_price": None,
        "is_listed": False,
        "listed_at": None,
        "is_verified": False,
        "verified_at": None,
        "created_at": current_time,
        "updated_at": current_time,
    }

    await db.order_item.update_document(order_item_id, insert_format)
