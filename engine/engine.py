import logging
from typing import Optional, List

from .config import Config
from .downloader import Downloader
from .response_handler import ResponseHandler
from .storage import Storage
from .task_queue import TaskQueue

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Engine:

    def __init__(self, config: Config):
        self._config = config
        self._downloader: Optional[Downloader] = config.downloader()
        self._response_handlers: List[ResponseHandler] = config.response_handlers()
        self._storage: Optional[Storage] = config.storage()

        self._task_queue = TaskQueue()

    def start(self):
        if self._downloader is None:
            logger.error('missing downloader')
            return

        if len(self._response_handlers) == 0:
            logger.error('missing response handler')
            return

        if self._storage is None:
            logger.error('missing storage')
            return

        for req in self._config.tasks():
            self._task_queue.append_pending_task(req)

        while True:
            req = None
            try:
                req = self._task_queue.pop_pending_task()
                if req is None:
                    break

                res = self._downloader.handle_request(req)

                for handler in self._response_handlers:
                    res = handler.handle_response(res)

                self._storage.storage(req, res)

                self._task_queue.append_finished_task(req)

            except Exception as e:
                logger.exception(e)
                if req is not None:
                    self._task_queue.append_failed_task(req)
