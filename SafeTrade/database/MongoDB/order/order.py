from datetime import datetime, timezone

from SafeTrade.database.MongoDB import MongoDb as db


async def saveAdminOrder(
    id,
    amount,
    email,
    password,
    backup_code,
    is_active=False,
    status="P",
    is_logged_in=False,
):
    """
    Initiate an order from admin
    """
    current_time = datetime.now(timezone.utc)
    existing_admin_order = await db.orders.get_document_by_kwargs(
        _id=id,
    )
    # P -> Proccessing
    # D -> Done
    # C -> Canceled
    allowed_statuses = ["P", "D", "C"]
    if status not in allowed_statuses:
        raise ValueError("Invalid admin order status")

    if existing_admin_order:
        insert_format = {
            "updated_at": current_time,
            "is_active": is_active,
            "is_logged_in": is_logged_in,
            "status": status,
        }
    else:
        insert_format = {
            "amount": amount,
            "status": status,
            "email": email,
            "password": password,
            "backup_code": backup_code,
            "is_logged_in": False,
            "is_active": is_active,
            "created_at": current_time,
            "updated_at": current_time,
        }

    await db.admin_order.update_document(id, insert_format)


async def saveOrder(order_id, user_id, admin_order_id, status="P"):
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
            "admin_order_id": admin_order_id,
            "status": status,
            "total_coins": 0,
            "created_at": current_time,
            "updated_at": current_time,
        }

    await db.orders.update_document(order_id, insert_format)


async def saveOrderItem(order_item_id, admin_order_id, supply: int):
    """
    save orderItem for an order
    """

    current_time = datetime.now(timezone.utc)

    insert_format = {
        "order_id": admin_order_id,
        "supply": supply,
        "card_amount": None,
        "buy_price": None,
        "sell_price": None,
        "is_listed": False,
        "listed_at": None,
        "has_bought": False,
        "bought_at": None,
        "is_verified": False,
        "verified_at": None,
        "created_at": current_time,
        "updated_at": current_time,
    }

    await db.order_item.update_document(order_item_id, insert_format)
