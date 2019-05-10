import io
import logging
import time
from functools import wraps

logger = logging.getLogger()
logger.addHandler(logging.NullHandler())


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logging.info(f'Function {func.__name__} cost {end - begin} seconds.')
        return result

    return wrapper


def typesetting(lines: list, indent: bool = True) -> str:
    dest = io.StringIO()
    for line in lines:
        line = typesetting_line(line, indent)
        dest.write(line)
    dest.seek(0)
    return dest.read()


def typesetting_line(line: str, first_indent: bool = True) -> str:
    line = line.strip()
    if first_indent:
        line = f'　　{line}\n'
    else:
        line = f'{line}\n'
    return line
