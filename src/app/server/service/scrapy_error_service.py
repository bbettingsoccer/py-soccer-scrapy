from fastapi.encoders import jsonable_encoder

from ...server.dao.operationimpl_dao import OperationImplDAO
from ...server.model.scrapy_error_model import ScrapyErrorModel


class ScrapyErrorService:

    def __init__(self, collection_name: str):
        self.db = OperationImplDAO(collection_name)

    async def getErrorByCollection(self):
        objectL = []
        try:
            objects = await self.db.find_condition(None)
            if objects:
                for objected in objects:
                    objectL.append(ScrapyErrorModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("[Error :: getCollectionByName] - Find-Collection ", e)
        return None

    async def getCollectionName(self):
        objectL = []
        try:
            objects = await self.db.list_all_collection()
            print("getCollectionName ", objects)

            return objects
        except Exception as e:
            print("[Error :: getCollectionByName] - Find-Collection ", e)
        return None


    async def save(self, data: ScrapyErrorModel):
        try:
            jsonObj = jsonable_encoder(data)
            await self.db.save(jsonObj)
            return True
        except Exception as e:
            print("[Error]::[ScrapyErrorService] - Save ", e)
            raise


    async def dropCollection(self):
        try:
            return await self.db.remove_collection()
        except Exception as e:
            print("[Error]::[ScrapyErrorService] - dropCollection ", e)
            return False
