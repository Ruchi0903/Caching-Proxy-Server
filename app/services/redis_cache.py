import json
import redis
from typing import Any

from app.services.base_cache import BaseCache

class RedisCache(BaseCache):
    def __init__(self, redis_url: str):
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)

    def get(self, key: str) -> Any:
        value = self.client.get(key)
        if value is None:
            return None
        return json.loads(value)
    
    def set(self, key: str, value: Any, ttl: int):
        self.client.setex(key, ttl, json.dumps(value))

    def clear(self):
        self.client.flushdb()