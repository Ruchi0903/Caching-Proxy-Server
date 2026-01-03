from fastapi import APIRouter, Query, HTTPException, Response
import httpx
from app.core.config import get_cache_ttl, get_upstream_base_url

from app.services.cache import cache

router = APIRouter()

# CACHE_TTL = 60 #seconds

@router.get("/proxy")
async def proxy_response(response: Response, url: str = Query(..., description="Upstream URL")):
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
        response.headers["X-Cache"] = "HIT"
        return {
            "success": True,
            "source": "cache",
            "data": cached_response,
        }
    
    # 3. Cache miss -> call upstream
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
        
        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail="Upstream server returned an error",
            )
        
        data = response.json()

        # 4. Store in cache
        cache.set(cache_key, data, get_cache_ttl())
        response.headers["X-Cache"] = "MISS"
        return {
            "succes": True,
            "source": "upstream",
            "data": data,
        }
    
    except httpx.RequestError:
        raise HTTPException(status_code=400, detail="Invalid or unreachable upstream URL")
    

@router.delete("/cache")
def clear_cache():
    cache.clear()
    return {"success": True, "message": "Cache cleared successfully"}
    


# APIRouter() - like express.Router()
# Query - used to explicitly define query params, fastapi is strict, hence we need to use it.
# HTTPException - like res.status(400).json({...}); fastapi way of throwing http errors.
# httpx - axios equivalent; modern, async, built for fastapi

# @router.get("/proxy") = router decorator in python => similar to func chaining in express.js = router.get("/proxy", async(req, res)) => {}
# async def proxy_response(url: str = Query(..., description="Upstream URL")): => similar to async function proxyResponse(req, res) {const url = req.query.url}
# async def = enables await
# url: str = tells that url should be a string; fastapi uses this for validation, swagger docs, auto error handling 
# Query(...) = means this comes from query params; ... = required parameter; if user doesn't pass ?url=, fastapi auto-throws 422 error
# async with httpx.AsyncClient() as client: => like const axios = require("axios"); But better.
# "async with" - automatically opens + closes connection, no memory leaks.
# response = await client.get(url) => similar to: const response = await axios.get(url);
# return {"upstream_status": response.status_code,"data": response.json()} => similar to res.json({upstream_status: response.status, data: response.data})
# fastapi automatically json-serializes dicts, no res.json() needed.
# except httpx.RequestError: raise HTTPException(status_code=400, detail="Invalid...") => similar to catch(err){res.status(400).json({message: "Invalid..."})}