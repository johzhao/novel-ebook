import logging

import requests

from engine.downloader import Downloader
from engine.request import Request
from engine.response import Response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SimpleDownloader(Downloader):

    def __init__(self):
        self._session = requests.session()
        self._headers = {
            'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/86.0.4240.75 Safari/537.36')
        }
        pass

    def handle_request(self, request: Request) -> Response:
        resp = requests.get(request.url, headers=self._headers)

        if resp.status_code != 200:
            raise Exception((f'Request {request.url} failed with status code {resp.status_code}, '
                             f'reason {resp.reason}'))

        response = Response(request, resp.text)

        return response
