

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.till import router

app = FastAPI(title="Sokoni Change-Maker", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def health():
    return {"status": "ok", "service": "sokoni-change-maker"}
