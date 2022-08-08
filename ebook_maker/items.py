# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EbookItem(scrapy.Item):
    source = scrapy.Field()
    book_id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()


class EbookChapterItem(scrapy.Item):
    source = scrapy.Field()
    book_id = scrapy.Field()
    chapter_id = scrapy.Field()
    title = scrapy.Field()
    paragraphs = scrapy.Field()
