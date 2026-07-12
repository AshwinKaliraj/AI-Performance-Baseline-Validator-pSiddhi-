from fastapi import FastAPI, Request
import time

from app.routers import (
    health,
    user,
    payment,
    order,
    metrics,
    baseline,
    anomaly,
    risk,
    validation,
    analyze,
    history,
    ai_analysis
)

from app.utils.prometheus_metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    ERROR_COUNT
)

app=FastAPI(
    title="AI Performance Baseline Validator",
    version="1.0.0"
)


@app.middleware("http")
async def prometheus_middleware(request:Request,call_next):

    start_time=time.perf_counter()

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()

    try:

        response=await call_next(request)
        return response

    except Exception:

        ERROR_COUNT.labels(
            method=request.method,
            endpoint=request.url.path
        ).inc()

        raise

    finally:

        duration=time.perf_counter()-start_time

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)


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
app.include_router(ai_analysis.router)