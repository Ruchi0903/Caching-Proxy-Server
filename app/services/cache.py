import time
from typing import Any, Dict
from app.services.base_cache import BaseCache
import os
from app.services.redis_cache import RedisCache
import logging

logger = logging.getLogger(__name__)

class InMemoryCache(BaseCache):
    def __init__(self):
        self._store: Dict[str, Dict[str , Any]] = {}
    
    def get(self, key: str):
        entry = self._store.get(key)

        if not entry:
            return None
        
        if entry["expires_at"] < time.time():
            # cache expired -> delete it
            del self._store[key]
            return None
        
        return entry["value"]
    
    def set(self, key: str, value: Any, ttl: int):
        expires_at = time.time() + ttl

        self._store[key] = {
            "value": value,
            "expires_at": expires_at,
        }
    
    def clear(self):
        self._store.clear()

CACHE_BACKEND = os.getenv("CACHE_BACKEND", "memory")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

if CACHE_BACKEND == "redis":
    cache = RedisCache(REDIS_URL)
    logger.info("Using Redis cache backend")
else:
    cache = InMemoryCache()
    logger.info("Using in-memory cache backend")
