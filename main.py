import scrapy.crawler
import scrapy.utils.project

import ebook_maker.spiders.dizishu


def main():
    settings = scrapy.utils.project.get_project_settings()
    process = scrapy.crawler.CrawlerProcess(settings)
    process.crawl(ebook_maker.spiders.dizishu.DiZiShuSpider)
    process.start()


if __name__ == '__main__':
    main()
