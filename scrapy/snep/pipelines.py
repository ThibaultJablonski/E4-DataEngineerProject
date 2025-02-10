import pymongo
from snep.items import AlbumItem, ArtisteItem, LabelItem, CertificationItem

class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI", "mongodb://mongo:27017"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "snep")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """ Insère chaque type d'item dans la bonne collection MongoDB. """
        item_dict = dict(item)  # Convertit l'item en dictionnaire

        if isinstance(item, AlbumItem):
            self.db["albums"].update_one(
                {"_id": item_dict["_id"]}, {"$set": item_dict}, upsert=True
            )
        elif isinstance(item, ArtisteItem):
            self.db["artistes"].update_one(
                {"_id": item_dict["_id"]}, {"$set": item_dict}, upsert=True
            )
        elif isinstance(item, LabelItem):
            self.db["labels"].update_one(
                {"_id": item_dict["_id"]}, {"$set": item_dict}, upsert=True
            )
        elif isinstance(item, CertificationItem):
            self.db["certifications"].update_one(
                {"_id": item_dict["_id"]}, {"$set": item_dict}, upsert=True
            )

        return item
