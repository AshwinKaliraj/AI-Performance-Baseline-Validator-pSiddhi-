from fastapi import FastAPI
from app.routers import health,user,payment,order,metrics,baseline,anomaly,risk,validation,analyze,history
app=FastAPI(
    title="AI Performance Baseline Validator",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(user.router)
app.include_router(payment.router)
app.include_router(order.router)
app.include_router(metrics.router)
app.include_router(baseline.router)
app.include_router(anomaly.router)
app.include_router(risk.router)
app.include_router(validation.router)
app.include_router(analyze.router)
app.include_router(history.router)