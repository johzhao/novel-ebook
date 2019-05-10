# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelSummaryItem(scrapy.Item):
    nid = scrapy.Field()
    index = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    tags = scrapy.Field()


class NovelItem(scrapy.Item):
    nid = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
