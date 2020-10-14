import logging
from typing import Optional

from .request import Request

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class TaskQueue:

    def __init__(self):
        pass

    def push_task(self, request: Request):
        pass

    def pop_task(self) -> Optional[Request]:
        pass
