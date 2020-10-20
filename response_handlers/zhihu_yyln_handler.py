import logging

from engine.response import Response
from engine.response_handler import ResponseHandler

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ZhiHuYYLNHandler(ResponseHandler):

    def __init__(self):
        pass

    def handle_response(self, response: Response) -> Response:
        return response
