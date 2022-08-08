from typing import Optional

import pymongo
import pymongo.database
import scrapy.spiders

import ebook_maker.items
from exporter.epub.epub_creator import EPubCreator


class ExportEPubPipeline:
    collection_name = 'scrapy_items'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
                   temp_folder=crawler.settings.get('TEMP_FOLDER', './temp'),
                   output_folder=crawler.settings.get('OUTPUT_FOLDER', './output'))

    def __init__(self, mongo_uri: str, mongo_db: str, temp_folder: str, output_folder: str):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.temp_folder = temp_folder
        self.output_folder = output_folder
        self.client = None  # type: Optional[pymongo.MongoClient]
        self.db = None  # type: Optional[pymongo.database.Database]
        self.books = {
            'dizishu': [
                '10601',
            ]
        }

    # noinspection PyUnusedLocal
    def open_spider(self, spider: scrapy.spiders.Spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # noinspection PyUnusedLocal
    def close_spider(self, spider: scrapy.spiders.Spider):
        self._export_books()
        self.client.close()

    # noinspection PyUnusedLocal
    def process_item(self, item: scrapy.Item, spider: scrapy.spiders.Spider):
        if isinstance(item, ebook_maker.items.EbookItem):
            source = item.get("source", "")
            book_id = item.get("book_id", "")
            if source not in self.books:
                self.books[source] = []
            if book_id not in self.books[source]:
                self.books[source].append(book_id)

        return item

    def _export_books(self):
        for source, book_ids in self.books.items():
            for book_id in book_ids:
                book_summary = self.db[source].find_one({'book_id': book_id})
                epub_creator = EPubCreator(self.output_folder)
                epub_creator.start_book(book_summary['name'], book_summary['author'], book_summary['source'],
                                        book_summary['description'])
                collection_name = f'{source}_{book_id}'
                for chapter in self.db[collection_name].find({}).sort('chapter_id'):
                    epub_creator.append_chapter(chapter['title'], chapter['paragraphs'])

                epub_creator.finish_book()
