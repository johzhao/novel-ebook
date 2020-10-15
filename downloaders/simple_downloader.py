import logging
import requests
from engine.request import Request
from engine.response import Response

from ..engine.downloader import Downloader

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SimpleDownloader(Downloader):

    def handle_request(self, request: Request) -> Response:
        resp = requests.get(request.url)

        if resp.status_code != 200:
            raise Exception((f'Request {request.url} failed with status code {resp.status_code}, '
                             f'reason {resp.reason}'))

        response = Response(request, resp.text)

        return response
