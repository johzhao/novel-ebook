import json
import re

import scrapy
import scrapy.http

import ebook_maker.items


class DiZiShuSpider(scrapy.Spider):
    name = 'dizishu'
    allowed_domains = ['www.dizishu.com']
    start_urls = []
    book_ids = [
        '17709',
    ]
    pattern = re.compile(r"cctxt=cctxt.replace\(/(.+)?/g,'(.+)?'\);")
    table_pattern = re.compile(r'<table.*</table>')

    def start_requests(self):
        for book_id in self.book_ids:
            url = f'https://www.dizishu.com/files/{book_id[:-3]}/{book_id}/{book_id}.json'
            yield scrapy.Request(url, dont_filter=True, callback=self.parse)

    def parse(self, response: scrapy.http.Response, **kwargs):
        # parse the catalog
        data = json.loads(response.text)
        info_data = data['info']
        book_id = info_data['articleid']
        yield ebook_maker.items.EbookItem(source=self.name, book_id=book_id, name=info_data['articlename'],
                                          author=info_data['author'], description=info_data['intro'].strip())

        for chapter in data['list']:
            chapter_id = chapter['chapterid']
            chapter_title = chapter['chaptername']
            chapter_url = f'https://www.dizishu.com/files/article/html555/{book_id[:-3]}/{book_id}/{chapter_id}.html'
            self.logger.info(f'request chapter by url {chapter_url}')

            request = scrapy.Request(chapter_url, callback=self.parse_body)
            request.cb_kwargs['book_id'] = book_id
            request.cb_kwargs['chapter_id'] = chapter_id
            request.cb_kwargs['chapter_title'] = chapter_title
            yield request

    def parse_body(self, response: scrapy.http.Response, book_id: str, chapter_id: str, chapter_title: str):
        # parse the main body
        contents = response.css('::text').getall()
        replaces = {
            'var cctxt=\'': '',
            '<content>': '',
            '</content>': '',
        }
        data = contents[-1]
        for match in self.pattern.findall(data):
            replaces[match[0]] = match[1]

        last_paragraph_index = len(contents) - 1
        paragraphs = []
        for index, paragraph in enumerate(contents):
            for key, value in replaces.items():
                paragraph = paragraph.replace(key, value)

            if index == last_paragraph_index:
                i = paragraph.rfind('\';\r\ncctxt=cctxt')
                paragraph = paragraph[:i]

            paragraph = self.table_pattern.sub('', paragraph)

            paragraph = paragraph.strip()

            if paragraph:
                paragraphs.append(paragraph)

        yield ebook_maker.items.EbookChapterItem(source=self.name, book_id=book_id, chapter_id=int(chapter_id),
                                                 title=chapter_title, paragraphs=paragraphs)
