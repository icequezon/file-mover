import os

from src.exceptions import MissingFileException
from src.logger import logger
from src.redis import RedisConnection
from src.mover import FileMover


REDIS_STREAM = os.getenv("REDIS_STREAM", "stream")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 55000)
REDIS_CONSUMER_GROUP = os.getenv("REDIS_CONSUMER_GROUP", "file-mover")
REDIS_CONSUMER = os.getenv("REDIS_CONSUMER", "file-mover-1")
REDIS_FULL_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


class FileMoverWorker:
    def __init__(self, config):
        self.redis = RedisConnection(REDIS_FULL_URL, REDIS_STREAM)
        self.mover = FileMover(config)

    def process_messages(self, messages):
        for _, entries in messages:
            for _, data in entries:
                try:
                    self.mover.handle_event(data)
                except MissingFileException as e:
                    logger.debug("File not found. Skipping event.")
                except Exception as e:
                    logger.error(f"{repr(e)}")

    def run(self):
        self.redis.init_consumer_group(REDIS_CONSUMER_GROUP)
        while True:
            messages = self.redis.get_messages_from_consumer_group(REDIS_CONSUMER)
            self.process_messages(messages)
