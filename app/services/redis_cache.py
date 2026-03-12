import json
from typing import Any

from redis.asyncio import Redis
from app.services.base_cache import BaseCache


class RedisCache(BaseCache):
    def __init__(self, redis_url: str):
        self.client = Redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Any:
        value = await self.client.get(key)
        if value is None:
            return None
        return json.loads(value)
    
    async def set(self, key: str, value: Any, ttl: int):
        await self.client.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str) -> bool:
        result = await self.client.delete(key)
        return result > 0

    async def clear(self):
        await self.client.flushdb()