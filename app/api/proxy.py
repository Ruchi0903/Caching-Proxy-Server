from fastapi import APIRouter, Query, HTTPException, Response
import httpx
import logging
from app.core.config import get_cache_ttl, get_upstream_base_url
from app.core.metrics import metrics

from app.services.cache import cache

router = APIRouter()
logger = logging.getLogger(__name__)

# CACHE_TTL = 60 #seconds

@router.get("/proxy")
async def proxy_response(response: Response, url: str = Query(..., description="Upstream URL")):
    logger.info(f"Incoming proxy request for url={url}")
    metrics.record_request()

    base_url = get_upstream_base_url()

    if not url.startswith("http"):
        if not base_url:
            raise HTTPException(
                status_code=400,
                detail="Relative URL provided but no UPSTREAM_BASE_URL configured",
            )
        url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"

    # 1. Generate cache key
    # cache_key = url
    cache_key = f"GET:{url}"

    # 2. Check cache
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        logger.info(f"Cache HIT for key={cache_key}")
        metrics.record_cache_hit()
        response.headers["X-Cache"] = "HIT"
        return {
            "success": True,
            "source": "cache",
            "data": cached_response,
        }
    
    # 3. Cache miss -> call upstream
    logger.info(f"Cache MISS for key={cache_key}. Fetching from upstream.")
    metrics.record_cache_miss()

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
        
        logger.info(f"Upstream request successful for url={url}")
        
        if response.status_code >= 400:
            logger.error(f"Upstream request failed for url={url}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Upstream server returned an error",
            )
        
        data = response.json()

        # 4. Store in cache
        cache.set(cache_key, data, get_cache_ttl())
        response.headers["X-Cache"] = "MISS"
        
        logger.info(f"Upstream request successful for url={url}")

        return {
            "success": True,
            "source": "upstream",
            "data": data,
        }
    
    except httpx.RequestError:
        logger.error(f"Upstream request unreachable for url={url}")
        raise HTTPException(status_code=400, detail="Invalid or unreachable upstream URL")
    

@router.delete("/cache")
def clear_cache():
    cache.clear()
    logger.info("Cache cleared manually")
    return {"success": True, "message": "Cache cleared successfully"}

@router.get("/metrics")
def get_metrics():
    return{
        "success": True,
        "metrics": metrics.snapshot()
    }