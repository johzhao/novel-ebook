import abc
import logging

from .response import Response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ResponseHandler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle_response(self, response: Response) -> Response:
        pass
