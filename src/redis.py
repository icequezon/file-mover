import redis
import time

from src.logger import logger
from src import constants


class RedisConnection:
    def __init__(self, redis_full_url, stream_name):
        self.redis_stream_name = stream_name
        self.redis_client = redis.Redis.from_url(redis_full_url)
        self.redis_consumer_group = None

    def init_consumer_group(self, consumer_group):
        try:
            logger.info(f"Creating group {consumer_group}")
            self.redis_client.xgroup_create(
                self.redis_stream_name, consumer_group, id="$", mkstream=True
            )
            logger.info(f"Created group {consumer_group}")
        except redis.exceptions.ResponseError as e:
            if constants.REDIS_GROUP_ALREADY_CREATED in str(e):
                print("Group already exists, continuing...")
            else:
                raise
        finally:
            self.redis_consumer_group = consumer_group

    def get_messages_from_consumer_group(self, consumer_name, consumer_group=None):
        if not self.redis_consumer_group:
            self.init_consumer_group(consumer_group)
        return self.redis_client.xreadgroup(
            self.redis_consumer_group,
            consumer_name,
            {self.redis_stream_name: ">"},
            block=5000,
            count=100,
        )

    def ack_message(self, message_id):
        self.redis_client.xack(
            self.redis_stream_name, self.redis_consumer_group, message_id
        )

    def has_been_idle(self, threshold_seconds=1):
        pending = self.redis_client.xpending(
            self.redis_stream_name, self.redis_consumer_group
        )
        last_id = pending.get("max")

        if last_id is None:
            last_messages = self.redis_client.xrevrange(self.redis_stream_name, count=1)
            if not last_messages:
                return True
            last_id = last_messages[0][0]

        last_ms = int(last_id.decode().split("-")[0])
        current_ms = int(time.time() * 1000)

        if (current_ms - last_ms) >= threshold_seconds * 1000:
            return True
        return False
