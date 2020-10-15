import logging
from typing import Optional
import redis

from .request import Request

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class TaskQueue:
    PENDING_TASK_KEY = 'pending_tasks'
    FINISHED_TASK_KEY = 'finished_tasks'
    FAILED_TASK_KEY = 'failed_tasks'

    def __init__(self):
        # TODO: Pass the config by parameters
        self._pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self._redis = redis.Redis(connection_pool=self._pool)

    def append_pending_task(self, request: Request):
        with self._redis:
            self._redis.lpush(self.PENDING_TASK_KEY, request.serialize())

    def append_finished_task(self, request: Request):
        with self._redis:
            self._redis.lpush(self.FINISHED_TASK_KEY, request.serialize())

    def append_failed_task(self, request: Request):
        with self._redis:
            self._redis.lpush(self.FAILED_TASK_KEY, request.serialize())

    def get_pending_task(self) -> Optional[Request]:
        with self._redis:
            data = self._redis.lpop(self.PENDING_TASK_KEY)
            if data:
                req = Request()
                req.deserialize(data)
                return req
            return None
