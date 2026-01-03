# 🧠 Caching Proxy Server (FastAPI)
## Overview
This project is an HTTP caching proxy server built using FastAPI.
It intercepts client requests, checks an in-memory cache with TTL-based expiration, and forwards cache-miss requests to an upstream API.

The goal of this project is to demonstrate backend system design concepts such as request forwarding, caching strategies, cache invalidation, and clean service separation.

## Features
1. HTTP proxy endpoint to forward requests to upstream APIs
2. In-memory caching with TTL-based expiration
3. Automatic cache invalidation after TTL expiry
4. Manual cache invalidation endpoint
5. Asynchronous upstream requests using httpx
6. Clean separation between API layer and cache logic
7. Consistent response structure and error handling

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

**DELETE /cache**

Clears all cached responses.

Response
{
  "success": true,
  "message": "Cache cleared successfully"
}

Cache Behavior
1. Cached responses are stored in memory
2. Each cache entry has a configurable TTL
3. Cache entries are automatically invalidated after expiry
4. Manual cache clearing is supported via API
5. Cache TTL can be configured using the `CACHE_TTL` environment variable
6. Defaults to 60 seconds if not provided.
7. Cache TTL can also be configured via CLI using the `--ttl` flag

### Tech Stack

Python

FastAPI

HTTPX

Uvicorn

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

### Future Improvements
1. Redis-based distributed cache
2. Support for additional HTTP methods
3. Rate limiting and observability

## EXTRAS
This repo serves as a solution to https://roadmap.sh/projects/caching-server
