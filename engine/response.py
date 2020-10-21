import logging

from .request import Request

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Response:

    def __init__(self, request: Request, content: str):
        self.request = request
        self.content = content
