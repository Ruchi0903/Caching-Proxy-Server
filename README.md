# 🧠 Caching Proxy Server (FastAPI)
## Overview
This project is an HTTP caching proxy server built using FastAPI.
It intercepts client requests, checks a cache with TTL-based expiration, and forwards cache-miss requests to an upstream API. The cache layer supports **both in-memory and Redis-based backends**, selectable at runtime.

The goal of this project is to demonstrate backend system design concepts such as request forwarding, caching strategies, cache invalidation, observability (logging & metrics), and clean service separation.

## Features
1. HTTP proxy endpoint to forward requests to upstream APIs
2. Pluggable cache backends:
  + In-memory cache (default)
  + Redis-based distributed cache
3. TTL-based cache expiration (ENV + CLI configurable)
4. Automatic cache invalidation after TTL expiry
5. Manual cache invalidation endpoint
6. Asynchronous upstream requests using httpx
7. Clean separation between API, cache, and upstream services
8. Consistent response structure and error handling
9. X-Cache response headers (HIT/MISS)
10. Structured logging for request flow and cache behavior
11. Internal metrics endpoint to monitor cache effectiveness

### API Endpoints
**GET /proxy**

Proxies a request to an upstream API and caches the response.

*Query Parameters*

url (string, required): Upstream API URL

Response
{
    "success": true,
    "source": "cache | upstream",
    "data": {...}
}

Response Headers
X-Cache: HIT | MISS

**DELETE /cache**

Clears all cached responses (in-memory or Redis).

Response
{
  "success": true,
  "message": "Cache cleared successfully"
}

**GET /metrics**

Exposes internal metrics for cache behavior

Response
{
  "success": true,
  "metrics": {
    "total_requests": 10,
    "cache_hits": 7,
    "cache_misses": 3,
    "cache_hit_ratio": 0.7
  }
}

Cache Behavior
1. Cached responses are stored using either in-memory or Redis backend
2. Cache backend is selected via environment variable:
  + CACHE_BACKEND=memory (default)
  + CACHE_BACKEND=redis 
3. Each cache entry has a configurable TTL
4. Cache entries are automatically invalidated after expiry
5. Manual cache clearing is supported via API
6. Cache TTL can be configured using the `CACHE_TTL` environment variable
7. Cache TTL can also be configured via CLI using the `--ttl` flag
8. Redis cache persists across application restarts

### Observability

#### Logging

Structured logs are emitted for:

  + Incoming proxy requests
  + Cache HIT/MISS events
  + Upstream request success and failure
  + Cache backend selection
  + Manual cache invalidation

#### Metrics

The service exposes internal metrics to measure:

  + Total requests
  + Cache hits
  + Cache misses
  + Cache hit ratio

This provides visibility into cache effectiveness and request patterns.

### Tech Stack

+ Python
+ FastAPI
+ HTTPX
+ Uvicorn
+ Redis

**How to Run Locally**

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

fastapi dev app/main.py

Access Swagger docs at: 
http://127.0.0.1:8000/docs

## CLI USAGE (Recommended)

This project also provides a simple CLI wrapper to start the caching proxy server with configurabel options such as port, upstream origin, and cache TTL.

**Start the server using CLI**

*python caching_proxy.py --port 3000 --origin https://dummyjson.com --ttl 15*

CLI Options
+ --port: Port number on which the proxy server should run (default: 8000)
+ --origin: Base upstream URL to proxy requests to (eg: https://dummyjson.com)
+ --ttl: Cache TTL (Time To Live) in seconds

*Example Usage*

After starting the server with:
*python caching_proxy.py --port 3000 --origin https://dummyjson.com --ttl 15*

You can make requests like:

GET http://127.0.0.1:3000/proxy?url=products

This request will be proxied to:

https://dummyjson.com/products

Cached responses will expire after 15 seconds.

You can see metrics at:

http://127.0.0.1:8000/metrics

### Redis Cache
To use Redis as the cache backend:

*CACHE_BACKEND=redis \
REDIS_URL=redis://localhost:6379 \
UPSTREAM_BASE_URL=https://dummyjson.com \
uvicorn app.main:app --reload*

Redis enables:
  + Distributed caching
  + Persistence across server starts
  + Production-ready cache behavior

## EXTRAS
This repository serves as a solution to https://roadmap.sh/projects/caching-server