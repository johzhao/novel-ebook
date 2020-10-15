from typing import Optional, List
import logging

from .task_queue import TaskQueue
from .downloader import Downloader
from .response_handler import ResponseHandler

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Engine:

    def __init__(self):
        # TODO: get the downloader and handlers by config
        self._downloader: Optional[Downloader] = None
        self._response_handlers: List[ResponseHandler] = []

        self._task_queue = TaskQueue()

    def start(self):
        if self._downloader is None:
            logger.error('missing downloader')
            return

        if len(self._response_handlers) == 0:
            logger.error('missing response handler')
            return

        req = None
        while True:
            try:
                req = self._task_queue.pop_pending_task()
                if req is None:
                    break

                res = self._downloader.handle_request(req)

                for handler in self._response_handlers:
                    res = handler.handle_response(res)

                # TODO: Store the result

                self._task_queue.append_finished_task(req)

            except Exception as e:
                logger.exception(e)
                if req:
                    self._task_queue.append_failed_task(req)
