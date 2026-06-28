from fastapi import FastAPI
from app.routers import health,user,payment,order
app=FastAPI(
    title="AI Performance Baseline Validator",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(user.router)
app.include_router(payment.router)
app.include_router(order.router)