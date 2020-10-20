import logging
from typing import List

from downloaders.simple_downloader import SimpleDownloader
from engine.config import Config
from engine.downloader import Downloader
from engine.request import Request
from engine.response_handler import ResponseHandler
from engine.storage import Storage
from response_handlers.zhihu_yyln_handler import ZhiHuYYLNHandler
from storages.simple_file_storage import SimpleFileStorage

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ZhiHuYYLNConfig(Config):

    def __init__(self):
        pass

    def downloader(self) -> Downloader:
        return SimpleDownloader()

    def response_handlers(self) -> List[ResponseHandler]:
        return [
            ZhiHuYYLNHandler(),
        ]

    def storage(self) -> Storage:
        return SimpleFileStorage()

    def tasks(self) -> List[Request]:
        request = Request()
        request.url = 'https://zhuanlan.zhihu.com/p/147779520'
        request.metadata['file_path'] = './htmls/147779520.html'
        return [
            request
        ]
