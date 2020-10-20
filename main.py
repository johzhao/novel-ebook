import logging

from configs import *
from engine.engine import Engine

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def main():
    config = ZhiHuYYLNConfig()
    engine = Engine(config)
    engine.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
