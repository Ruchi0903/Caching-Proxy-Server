import os
DEFAULT_CACHE_TTL = 60 #seconds

def get_cache_ttl() -> int:
    """
    Returns cache TTL from env variable if set, otherwise returns default value.
    """
    return int(os.getenv("CACHE_TTL", DEFAULT_CACHE_TTL))