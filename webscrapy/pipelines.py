# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import motor.motor_asyncio


class WebscrapyPipeline:
    db = None

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.client = None
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        print("from_crawler ")
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            collection_name=crawler.settings.get('COLLECTION_NAME')
        )

    def open_spider(self, spider):
        print("open_spider ")

        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri, maxpoolsize=500)
            self.db = self.client[self.mongo_db]
            self.db[self.collection_name].delete_many({})
        except Exception as e:
            print("Can´t not connect to the database :: ", e)
            return -1

    def close_spider(self, spider):
        print("close_spider ")
        self.client.close()

    def process_item(self, item, spider):
        print("process_item ")
        try:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
            return item
        except Exception as e:
            print("[Error :: Pipeline] - Process_item ", e)
            return -1

    def find_collection(self):
        print("close_spider ")
        try:
            if self.collection_name in self.db[self.collection_name].collection_names():
                print("++++++++++++++ Collection exists ++++++++++++++++")
        except Exception as e:
            print("[Error :: Pipeline] - Process_item ", e)
            return -1


