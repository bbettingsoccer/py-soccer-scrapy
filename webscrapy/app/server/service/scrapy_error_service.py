from fastapi.encoders import jsonable_encoder

from ...server.dao.operationimpl_dao import OperationImplDAO
from ...server.model.scrapy_response_model import ScrapyResponseModel


class ScrapyErrorService:

    def __init__(self, collection_name: str):
        print("COLLECTION -- NAME ", collection_name)
        self.db = OperationImplDAO(collection_name)

    async def getErrorByCollection(self):
        objectL = []
        try:
            objects = await self.db.find_condition(None)
            print("10000000000000000000000000 Find-Collection ", objects)

            if objects:
                for objected in objects:
                    objectL.append(ScrapyResponseModel.data_helper(objected))
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


    async def save(self, data: ScrapyResponseModel):
        try:
            jsonObj = jsonable_encoder(data)
            await self.db.save(jsonObj)
            return True
        except Exception as e:
            print("[Error]::[ScrapyErrorService] - Save ", e)
            raise


    def dropCollection(self):
        try:
            return self.db.remove_collection()
        except Exception as e:
            print("[Error]::[ScrapyErrorService] - dropCollection ", e)
            return False
