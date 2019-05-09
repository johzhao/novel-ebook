# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo

from novel.settings import mongo_db_host, mongo_db_port

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class NovelPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(mongo_db_host, mongo_db_port)
        self.database = self.client['novel']

    def process_item(self, item, _):
        data = dict(item)
        collection_name = data.get('host', 'unknown')
        data.pop('host', None)
        collection = self.database[collection_name]
        collection.insert(data)
        return item
