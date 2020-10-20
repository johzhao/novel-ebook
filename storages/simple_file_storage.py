import logging

from engine.request import Request
from engine.response import Response
from engine.storage import Storage

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SimpleFileStorage(Storage):

    def __init__(self):
        pass

    def storage(self, request: Request, response: Response):
        file_path = request.metadata.get('file_path', '')
        if not file_path:
            raise Exception(f'failed to get file_path from request {request}')

        with open(file_path, 'w') as output_file:
            output_file.write(response.content)
