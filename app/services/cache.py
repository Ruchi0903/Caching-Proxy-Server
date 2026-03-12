import time
from collections import OrderedDict
from typing import Any, Dict
from app.services.base_cache import BaseCache
import os
from app.services.redis_cache import RedisCache
import logging

logger = logging.getLogger(__name__)

DEFAULT_MAX_SIZE = 500  # max number of entries in the in-memory cache

class InMemoryCache(BaseCache):
    def __init__(self, max_size: int = DEFAULT_MAX_SIZE):
        self._store: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._max_size = max_size

    async def get(self, key: str):
        entry = self._store.get(key)

        if not entry:
            return None
        
        if entry["expires_at"] < time.time():
            # cache expired -> delete it
            del self._store[key]
            return None
        
        self._store.move_to_end(key)
        return entry["value"]
    
    async def set(self, key: str, value: Any, ttl: int):
        expires_at = time.time() + ttl

        if key in self._store:
            # Key exists — update and mark as most recently used
            self._store.move_to_end(key)
        elif len(self._store) >= self._max_size:
            # FIX: cache full — evict the least recently used item
            # popitem(last=False) removes from the FRONT = least recently used
            evicted_key, _ = self._store.popitem(last=False)
            logger.info(f"LRU eviction: removed key={evicted_key} (cache full at {self._max_size} entries)")

        self._store[key] = {
            "value": value,
            "expires_at": expires_at,
        }

    async def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False
    
    async def clear(self):
        self._store.clear()

CACHE_BACKEND = os.getenv("CACHE_BACKEND", "memory")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", DEFAULT_MAX_SIZE))

if CACHE_BACKEND == "redis":
    cache = RedisCache(REDIS_URL)
    logger.info("Using Redis cache backend")
else:
    cache = InMemoryCache(max_size=MAX_CACHE_SIZE)
    logger.info(f"Using in-memory cache backend (max_size={MAX_CACHE_SIZE})")
