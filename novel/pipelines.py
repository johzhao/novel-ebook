# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo

from novel.settings import mongo_db_host, mongo_db_port, novel_host

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class NovelPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(mongo_db_host, mongo_db_port)
        self.database = self.client['novel']
        self.collection = self.database[novel_host]

    def process_item(self, item, _):
        self.collection.insert(dict(item))
        return item
