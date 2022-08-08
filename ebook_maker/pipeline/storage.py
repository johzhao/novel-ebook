# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Optional

import pymongo
import pymongo.database
import scrapy.spiders
from itemadapter import ItemAdapter

import ebook_maker.items


class EbookStoragePipeline:
    collection_name = 'scrapy_items'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'))

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None  # type: Optional[pymongo.MongoClient]
        self.db = None  # type: Optional[pymongo.database.Database]

    # noinspection PyUnusedLocal
    def open_spider(self, spider: scrapy.spiders.Spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # noinspection PyUnusedLocal
    def close_spider(self, spider: scrapy.spiders.Spider):
        self.client.close()

    # noinspection PyUnusedLocal
    def process_item(self, item: scrapy.Item, spider: scrapy.spiders.Spider):
        if isinstance(item, ebook_maker.items.EbookItem):
            item = self._save_ebook_summary(item)
        if isinstance(item, ebook_maker.items.EbookChapterItem):
            item = self._save_ebook_item(item)

        return item

    def _save_ebook_summary(self, item: ebook_maker.items.EbookItem):
        collection_name = f'{item.get("source", "")}'
        self.db[collection_name].insert_one(ItemAdapter(item).asdict())
        return item

    def _save_ebook_item(self, item: ebook_maker.items.EbookChapterItem):
        collection_name = f'{item.get("source", "")}_{item.get("book_id", "")}'
        self.db[collection_name].insert_one(ItemAdapter(item).asdict())
        return item
