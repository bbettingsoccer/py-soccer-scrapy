from abc import ABC
from motor.core import AgnosticCollection
from .operation_dao import OperationDAO
from bson.objectid import ObjectId

from ..common.database import MongoManager


class OperationImplDAO(OperationDAO, ABC):
    instance_collection = None

    def __init__(self, collection):
        if collection is not None:
            self.collection = collection
            self.instance_collection = self.get_collection()
        else:
            print("AQUI ")
            self.instance_collection = self.get_instance_db()

    def get_instance_db(self) -> AgnosticCollection:
        database = MongoManager.getInstance()
        return database


    def get_collection(self) -> AgnosticCollection:
        database = MongoManager.getInstance()
        return database.get_collection(self.collection)

    async def save(self, data: dict) -> dict:
        print(" - - - SAVE - - - ", data)
        try:
            #loop = self.instance_collection.get_io_loop()
            #loop = asyncio.get_running_loop()
            #if loop and loop.is_running():
             #   tsk = loop.create_task(self.instance_collection.insert_one(data))
            await self.instance_collection.insert_one(data)
            return None
        except Exception as e:
            print('[Error]::[OperationImplDAO] - save > ', e)
            return None

    async def find_condition(self, filter) -> list[dict]:
        jsonList = []
        try:
            if filter is not None:
                async for objectFind in self.instance_collection.find(filter):
                    jsonList.append(objectFind)
            else:
                async for objectFind in self.instance_collection.find():
                    jsonList.append(objectFind)
            return jsonList
        except Exception as e:
            print('[Error]::[OperationImplDAO] - find_condition > ', e)
            return None

    async def find_one(self, id: str) -> dict:
        try:
            collectionObj = await self.instance_collection.find_one({"_id": ObjectId(id)})
            if collectionObj:
                return collectionObj
        except Exception as e:
            print('[Error]::[OperationImplDAO] - find_one > ', e)

    async def update_many(self, filter, data):
        try:
            await self.instance_collection.update_many(filter, {"$set": data})
            return True
        except Exception as e:
            print('[Error]::[OperationImplDAO] - update_many > ', e)
            return False

    async def update_one(self, id, data):
        try:
            print("UPDATE_ONE > ", data)
            await self.instance_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            return True
        except Exception as e:
            print('[Error]::[OperationImplDAO] - update_one > ', e)
            return False

    async def delete_condition(self, filter):
        try:
            await self.instance_collection.delete_many(filter)
            return True
        except Exception as e:
            print('[Error]::[OperationImplDAO] - delete_condition > ', e)
            return False

    def remove_collection(self):
        try:
            self.instance_collection.drop()
            return True
        except Exception as e:
            print('[Error]::[OperationImplDAO] - drop_collection > ', e)
            return False


    async def list_all_collection(self):
        try:
            collections = await self.instance_collection.list_collection_names()
            return collections
        except Exception as e:
            print('[Error]::[OperationImplDAO] - list_all_collection > ', e)
            return False


