# -*- coding: utf-8 -*-
import scrapy

from novel.items import NovelSummaryItem, NovelItem
from novel.settings import novel_ids, novel_host
from novel.utility import typesetting


class QidianSpider(scrapy.Spider):
    name = 'qidian_spider'

    allowed_domains = [
        'book.qidian.com',
        'read.qidian.com',
    ]

    def start_requests(self):
        if self.name.find(novel_host) != 0:
            raise ValueError(f'{self.name} was not used for {novel_host}')

        for book_id in novel_ids:
            meta = {
                'novel_id': book_id
            }
            url = f'https://book.qidian.com/info/{book_id}'
            yield scrapy.Request(url, callback=self.parse_chapters, meta=meta)

    def parse(self, response):
        pass

    def parse_chapters(self, response):
        meta = response.meta
        book_info_node = response.xpath('//div[contains(@class, "book-info")]')
        book_description = response.xpath('//div[contains(@class, "book-intro")]/p/text()').extract()

        summary_item = NovelSummaryItem()
        summary_item['nid'] = meta.get('novel_id', '')
        summary_item['index'] = 0
        summary_item['name'] = book_info_node.xpath('./h1/em/text()').get()
        summary_item['author'] = book_info_node.xpath('./h1/span/a/text()').get()
        summary_item['tags'] = book_info_node.xpath('./p/a[@class="red"]/text()').extract()

        summary_item['description'] = typesetting(book_description, False)
        yield summary_item

        chapter_elements = response.xpath('//div[@class="volume"]//ul[@class="cf"]/li')
        for index, chapter_element in enumerate(chapter_elements, 1):
            meta['index'] = index
            chapter_url = chapter_element.xpath('./a/@href').get()
            yield scrapy.Request(url=response.urljoin(chapter_url), callback=self.parse_one_chapter, meta=meta)

    def parse_one_chapter(self, response):
        meta = response.meta
        content_elements = response.xpath('//div[@class="read-content j_readContent"]/p/text()').extract()

        item = NovelItem()
        item['nid'] = meta['novel_id']
        item['index'] = meta['index']
        item['title'] = response.xpath('//div[@class="text-head"]/h3/text()').get()
        item['content'] = typesetting(content_elements, True)
        yield item
