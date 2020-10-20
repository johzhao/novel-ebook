import abc
import logging
from typing import List

from engine.downloader import Downloader
from engine.response_handler import ResponseHandler
from engine.storage import Storage
from engine.request import Request

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Config(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def downloader(self) -> Downloader:
        return NotImplemented

    @abc.abstractmethod
    def response_handlers(self) -> List[ResponseHandler]:
        return NotImplemented

    @abc.abstractmethod
    def storage(self) -> Storage:
        return NotImplemented

    @abc.abstractmethod
    def tasks(self) -> List[Request]:
        return NotImplemented
