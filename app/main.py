from fastapi import FastAPI
from app.routers import health

app=FastAPI(
    title="AI Performance Baseline Validator",
    version="1.0.0"
)

app.include_router(health.router)