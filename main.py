import pymongo
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from epub.epub_creator import EPubCreator
from novel.settings import novel_host, novel_ids, mongo_db_host, mongo_db_port
from novel.spiders.qidian_spider import QidianSpider
from novel.utility import timethis


def crawl_novels():
    process = CrawlerProcess(get_project_settings())
    process.crawl(QidianSpider)
    process.start()


def make_epubs():
    client = pymongo.MongoClient(host=mongo_db_host, port=mongo_db_port)
    db = client['novel']
    my_set = db[novel_host]

    for novel_id in novel_ids:
        creator = EPubCreator('./output')
        chapters = my_set.find({'nid': novel_id}).sort('index')
        summary = chapters[0]
        creator.start_book(summary['name'], summary['author'], '起点', summary['description'], summary['tags'])
        for chapter in chapters[1:]:
            creator.append_chapter(chapter['title'], chapter['content'])
        creator.finish_book()


@timethis
def main():
    crawl_novels()
    make_epubs()


if __name__ == '__main__':
    main()
