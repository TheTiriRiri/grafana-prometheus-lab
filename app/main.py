import asyncio
import random
import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
import structlog

from logging_config import setup_logging
from metrics import (
    HTTP_REQUEST_DURATION,
    HTTP_REQUESTS_TOTAL,
    MEMORY_LEAK_BYTES,
    ORDERS_PROCESSING_SECONDS,
    ORDERS_TOTAL,
    PRODUCTS_IN_STOCK,
)
from simulate import router as simulate_router, simulation_state

setup_logging()
logger = structlog.get_logger()

app = FastAPI(title="Shop API - Monitoring Lab")
app.include_router(simulate_router)

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 2999.99, "stock": 10},
    {"id": 2, "name": "Klawiatura", "price": 149.99, "stock": 50},
    {"id": 3, "name": "Mysz", "price": 79.99, "stock": 100},
    {"id": 4, "name": "Monitor", "price": 1299.99, "stock": 15},
    {"id": 5, "name": "Słuchawki", "price": 199.99, "stock": 30},
]

PRODUCTS_IN_STOCK.set(sum(p["stock"] for p in PRODUCTS))


class OrderRequest(BaseModel):
    product_id: int
    quantity: int = 1


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    if simulation_state.memory_leak_enabled:
        simulation_state._leak_store.append("x" * 102400)
        MEMORY_LEAK_BYTES.set(len(simulation_state._leak_store) * 102400)

    if request.url.path == "/metrics":
        return await call_next(request)

    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    HTTP_REQUESTS_TOTAL.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()
    HTTP_REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    return response


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/products")
async def list_products():
    request_id = uuid.uuid4().hex[:8]

    if simulation_state.slow_enabled:
        await asyncio.sleep(random.uniform(0.5, 2.0))

    if simulation_state.errors_enabled and random.random() < 0.3:
        logger.error("random_error", request_id=request_id, endpoint="/products")
        raise HTTPException(status_code=500, detail="Internal server error")

    logger.info(
        "products_listed",
        request_id=request_id,
        endpoint="/products",
        count=len(PRODUCTS),
    )
    return {"products": PRODUCTS}


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    request_id = uuid.uuid4().hex[:8]

    if simulation_state.slow_enabled:
        await asyncio.sleep(random.uniform(0.1, 1.0))

    if simulation_state.errors_enabled and random.random() < 0.3:
        logger.error(
            "random_error",
            request_id=request_id,
            endpoint=f"/products/{product_id}",
        )
        raise HTTPException(status_code=500, detail="Internal server error")

    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        logger.warning(
            "product_not_found",
            request_id=request_id,
            product_id=product_id,
        )
        raise HTTPException(status_code=404, detail="Product not found")

    logger.info("product_found", request_id=request_id, product_id=product_id)
    return product


@app.post("/orders")
async def create_order(order: OrderRequest):
    request_id = uuid.uuid4().hex[:8]
    start = time.time()

    delay = random.uniform(0.1, 0.5)
    if simulation_state.slow_enabled:
        delay = random.uniform(1.0, 5.0)
    await asyncio.sleep(delay)

    if simulation_state.errors_enabled and random.random() < 0.3:
        logger.error(
            "order_failed",
            request_id=request_id,
            endpoint="/orders",
            product_id=order.product_id,
        )
        raise HTTPException(status_code=500, detail="Order processing failed")

    duration = time.time() - start
    ORDERS_TOTAL.inc()
    ORDERS_PROCESSING_SECONDS.observe(duration)

    logger.info(
        "order_created",
        request_id=request_id,
        product_id=order.product_id,
        quantity=order.quantity,
        duration=round(duration, 3),
    )
    return {
        "order_id": uuid.uuid4().hex[:8],
        "status": "created",
        "processing_time": round(duration, 3),
    }
