import json
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Request:

    def __init__(self):
        self.url = ''
        self.headers = {}

    def serialize(self) -> str:
        obj = vars(self)
        return json.dumps(obj, ensure_ascii=False, sort_keys=True)

    def deserialize(self, data: str):
        obj = json.loads(data)
        self.__dict__.update(obj)
