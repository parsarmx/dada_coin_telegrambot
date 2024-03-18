from pprint import pprint

from Soheil.database import MongoDB as db
from Soheil.database.MongoDB import database


async def is_amount_valid(admin_order_id, amount):
    """
    this function checks if amount is less than
    finished user orders supply
    """
    pipeline = [
        {"$match": {"admin_order_id": admin_order_id, "has_bought": True}},
        {"$group": {"_id": None, "total": {"$sum": "$buy_price"}}},
    ]
    cursor = database.order_item.aggregate(pipeline)
    async for document in cursor:
        total_sum = document.get("total", 0)
        return total_sum
