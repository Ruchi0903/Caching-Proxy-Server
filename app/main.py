from fastapi import FastAPI
from app.api.proxy import router as proxy_router

app = FastAPI()

@app.get("/")
def health_check():
    return {"status" : "ok"}

app.include_router(proxy_router)