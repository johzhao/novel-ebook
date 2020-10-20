import abc
import logging

from .request import Request
from .response import Response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Storage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def storage(self, request: Request, response: Response):
        return NotImplemented
