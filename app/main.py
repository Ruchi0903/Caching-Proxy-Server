from fastapi import FastAPI
from app.api.proxy import router as proxy_router
from app.core.logging import setup_logging

app = FastAPI()

setup_logging()

@app.get("/")
def health_check():
    return {"status" : "ok"}

app.include_router(proxy_router)