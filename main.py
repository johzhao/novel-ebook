import scrapy.cmdline

from novel.settings import novel_host

if __name__ == '__main__':
    spider_name = f'{novel_host}_spider'
    scrapy.cmdline.execute(f'scrapy crawl {spider_name}'.split())
