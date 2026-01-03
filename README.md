🧠 Caching Proxy Server (FastAPI)
Overview
This project is an HTTP caching proxy server built using FastAPI.
It intercepts client requests, checks an in-memory cache with TTL-based expiration, and forwards cache-miss requests to an upstream API.

The goal of this project is to demonstrate backend system design concepts such as request forwarding, caching strategies, cache invalidation, and clean service separation.

Features
1. HTTP proxy endpoint to forward requests to upstream APIs
2. In-memory caching with TTL-based expiration
3. Automatic cache invalidation after TTL expiry
4. Manual cache invalidation endpoint
5. Asynchronous upstream requests using httpx
6. Clean separation between API layer and cache logic
7. Consistent response structure and error handling

API Endpoints
GET /proxy
Proxies a request to an upstream API and caches the response.
Query Parameters
url (string, required): Upstream API URL
Response
{
    "success": true,
    "source": "cache | upstream",
    "data": {...}
}

DELETE /cache
Clears all cached responses.
Response
{
  "success": true,
  "message": "Cache cleared successfully"
}

Cache behavior
1. Cached responses are stored in memory
2. Each cache entry has a configurable TTL
3. Cache entries are automatically invalidated after expiry
4. Manual cache clearing is supported via API
5. Cach TTL can be configured using the `CACHE_TTL` environment variable
6. Defaults to 60 seconds if not provided.
7. CACHE_TTL=10 uvicorn app.main:app --reload -> this will set the cache ttl to be 10 seconds, if not given anything, the default is 60 seconds.

Tech Stack
FastAPI

How to Run Locally
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py

Access Swagger docs at: 
http://127.0.0.1:8000/docs

Future Improvements
1. Redis-based distributed cache
2. Support for additional HTTP methods
3. Rate limiting and observability