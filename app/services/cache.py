# The cache service here shoud expose exactly these abilities:
# 1. get(key) -> return cached response or None
# 2. set(key, value, ttl) -> store response
# 3. clear() -> delete everything

import time
from typing import Any, Dict

class InMemoryCache:
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

cache = InMemoryCache()


# time = used to get current time like Date.now()
# typing = only for developer clarity, doesn't affect runtime, like typescript types - but optional & not annoying
# class InMemoryCache -- defining the cache class
# __init__ = constructor; self = this; _store = actual cache; _ in _store = means don't touch this directly.
# get() method = cache read
# entry = self()._store.get(key) => similar to const entry = this._store[key]; => difference is, .get() returns None (better), Js returns undefined.
# time.time() = current UNIX timestamp in seconds.
# del self._store[key] return None => delete expired cache => expired entries are removed only when accessed
# return entry["value"] => similar to return entry.value; => cached response returned
# set() method = cache write; def set(self, key: str, value: Any, ttl: int): => similar to set(key, value, ttl) {
# expires_at = time.time() + ttl => similar to const expiresAt = (Date.now()/1000) + ttl;
# store data => self.store[key] = {"value": value, "expires_at": expires_at,}
# clear() method => deletes everything; use case: cli command, admin endpoint, debugging, rage moments
# Creating a singleton instance -> cache = InMemoryCache() => similar to module.exports = new InMemoryCache() => same cache instance shared everywhere, memory persists as long as app is running, app restart = cache wiped (expected)
