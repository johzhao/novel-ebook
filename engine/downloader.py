import abc
import logging

from .request import Request
from .response import Response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Downloader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle_request(self, request: Request) -> Response:
        return NotImplemented
