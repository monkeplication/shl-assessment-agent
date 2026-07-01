from fastapi import FastAPI

from app.router import router

app = FastAPI(
    title="SHL Assessment Agent",
    version="1.0.0",
)

app.include_router(router)