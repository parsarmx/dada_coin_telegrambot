from sys import exit as exiter

from motor.motor_asyncio import AsyncIOMotorClient

from Soheil.config import MONGO_URI
from Soheil.logs import LOGGER


class MongoDb:
    """
    MongoDb class to help with basic CRUD ( Create, Read, Delete, Update)
    operations of documents for a specific collection.
    """

    def __init__(self, collection):
        self.collection = collection

    async def read_document(self, document_id):
        """
        Read the document using document_id.
        """
        return await self.collection.find_one({"_id": document_id})

    async def update_document(self, document_id, updated_data):
        """
        Update as well as create document from document_id.
        """
        updated_data = {"$set": updated_data}
        await self.collection.update_one(
            {"_id": document_id}, updated_data, upsert=True
        )

    async def delete_document(self, document_id):
        """
        Delete the document using document_id from collection.
        """
        await self.collection.delete_one({"_id": document_id})

    async def total_documents(self):
        """
        Return total number of documents in that collection.
        """
        return await self.collection.count_documents({})

    async def get_all_id(self):
        """
        Return list of all document "_id" in that collection.
        """
        return await self.collection.distinct("_id")

    async def get_document_by_kwargs(self, **kwargs):
        """
        Return one document by kwargs
        """
        return await self.collection.find_one(kwargs)

    async def get_documents_by_kwargs(self, **kwargs):
        """
        Return documents matching the given kwargs
        """
        cursor = self.collection.find(kwargs)
        documents = await cursor.to_list(length=None)
        return documents


async def check_mongo_uri(MONGO_URI: str) -> None:
    try:
        mongo = AsyncIOMotorClient(MONGO_URI)
        await mongo.server_info()
    except:
        LOGGER(__name__).error(
            "Error in Establishing connection with MongoDb URI. Please enter valid uri in the config section."
        )
        exiter(1)


# Initiating MongoDb motor client
mongodb = AsyncIOMotorClient(MONGO_URI)

# Database Name (dc_telegrambot).
database = mongodb.dc_telegrambot

# init objects
users = MongoDb(database.users)
# we should use this insted of csv file for player_cards prices (PricePishe)
player_cards = MongoDb(database.player_cards)
orders = MongoDb(database.orders)
order_item = MongoDb(database.order_item)
chats = MongoDb(database.chats)
admin_order = MongoDb(database.admin_order)
