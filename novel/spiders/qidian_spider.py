# -*- coding: utf-8 -*-
import scrapy

from novel.items import NovelItem


class QidianSpider(scrapy.Spider):
    name = 'qidian_spider'

    allowed_domains = [
        'book.qidian.com',
        'read.qidian.com',
    ]

    start_urls = [
        # 'https://www.qidian.com/free/all?action=1&orderId=&page=1&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1',
        # 'https://book.qidian.com/info/23813',
        'https://book.qidian.com/info/1010983927',
    ]

    def parse(self, response):
        yield from self.parse_chapters(response)

    def parse_chapters(self, response):
        chapter_elements = response.xpath('//div[@class="volume"]//ul[@class="cf"]/li')
        for index, chapter_element in enumerate(chapter_elements, 1):
            # chapter_name = chapter_element.xpath('./a/text()').get()
            # self.logger.info(f'Chapter {chapter_name}')
            chapter_url = chapter_element.xpath('./a/@href').get()
            yield scrapy.Request(url=response.urljoin(chapter_url), callback=self.parse_one_chapter,
                                 meta={'index': index})

    def parse_one_chapter(self, response):
        title = response.xpath('//div[@class="text-head"]/h3/text()').get()
        meta = response.meta
        # self.logger.info(f'Index: {meta["index"]}Received: {title}')
        content_elements = response.xpath('//div[@class="read-content j_readContent"]/p/text()').extract()
        contents = []
        for element in content_elements:
            contents.append(element)

        item = NovelItem()
        item['host'] = 'qidian'
        item['index'] = meta['index']
        item['title'] = title
        item['content'] = '\n'.join(contents)
        yield item
