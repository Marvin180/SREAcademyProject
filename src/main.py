import asyncio
import random
import time

from fastapi import FastAPI, HTTPException, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from starlette.routing import Match

app = FastAPI()

# --- Prometheus Metrics Definitions ---
# Counter: monotonically increasing value (ideal for total requests or errors)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

# Histogram: observes value distributions in buckets (ideal for request latency)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)

# Gauge: value that can go up and down (ideal for active in-flight requests)
REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests currently in progress",
    ["method", "endpoint"],
)


def _get_endpoint_label(request: Request) -> str:
    """Resolve the FastAPI route template (e.g. '/get-customers/{customer}') to prevent high cardinality."""
    route = request.scope.get("route")
    if route is not None and hasattr(route, "path"):
        return route.path

    partial_match = None
    for candidate in request.app.routes:
        match, _ = candidate.matches(request.scope)
        if match is Match.FULL and hasattr(candidate, "path"):
            return candidate.path
        if match is Match.PARTIAL and partial_match is None and hasattr(candidate, "path"):
            partial_match = candidate.path

    return partial_match or "unmatched"


@app.middleware("http")
async def prometheus_metrics_middleware(request: Request, call_next):
    """Track request count, latency, and active in-flight requests for every route."""
    if request.url.path == "/metrics":
        return await call_next(request)

    method = request.method
    endpoint = _get_endpoint_label(request)

    REQUESTS_IN_PROGRESS.labels(method=method, endpoint=endpoint).inc()
    start_time = time.perf_counter()
    status = "500"

    try:
        response = await call_next(request)
        status = str(response.status_code)
        return response
    finally:
        duration = time.perf_counter() - start_time
        REQUESTS_IN_PROGRESS.labels(method=method, endpoint=endpoint).dec()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()


@app.get("/metrics", include_in_schema=False)
def metrics():
    """Expose application and Python runtime metrics in Prometheus text format."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/")
async def root():
    random_seconds = random.randrange(0, 2)
    await asyncio.sleep(random_seconds)
    return {"message": "Hello World"}

@app.get("/get-orders")
def get_orders():
    random_seconds = random.randrange(0, 5)
    time.sleep(random_seconds)

    list_of_orders = {
        "ORD-100234": {
            "customer": "Emily Carter",
            "email": "emily.carter@example.com",
            "status": "Shipped",
            "order_date": "2026-11-01T09:15:42Z",
            "items": [
                {"sku": "SKU-1001", "name": "Wireless Mouse", "quantity": 1, "unit_price": 24.99},
                {"sku": "SKU-2040", "name": "USB-C Cable 2m", "quantity": 2, "unit_price": 9.50},
            ],
            "total": 43.99,
            "currency": "USD",
            "shipping_address": "123 Maple St, Austin, TX 78701, US",
            "payment_method": "Credit Card",
        },
        "ORD-100235": {
            "customer": "Michael Johnson",
            "email": "m.johnson@example.com",
            "status": "Processing",
            "order_date": "2026-11-02T14:03:10Z",
            "items": [
                {"sku": "SKU-3302", "name": "Mechanical Keyboard", "quantity": 1, "unit_price": 89.00},
                {"sku": "SKU-1001", "name": "Wireless Mouse", "quantity": 1, "unit_price": 24.99},
                {"sku": "SKU-4410", "name": "Monitor Stand", "quantity": 1, "unit_price": 34.50},
            ],
            "total": 148.49,
            "currency": "USD",
            "shipping_address": "45 Oak Ave, Denver, CO 80203, US",
            "payment_method": "PayPal",
        },
        "ORD-100236": {
            "customer": "Sofia Martinez",
            "email": "sofia.martinez@example.com",
            "status": "Delivered",
            "order_date": "2026-10-28T18:47:29Z",
            "items": [
                {"sku": "SKU-5120", "name": "Laptop Backpack", "quantity": 1, "unit_price": 59.90},
            ],
            "total": 59.90,
            "currency": "USD",
            "shipping_address": "78 Pine Rd, Miami, FL 33101, US",
            "payment_method": "Credit Card",
        },
    }

    return list_of_orders

@app.get("/get-customers")
def get_customers():
    random_seconds = random.randrange(0, 5)
    time.sleep(random_seconds)

    list_of_customers = {
        "CUST-5001": {
            "name": "Emily Carter",
            "email": "emily.carter@example.com",
            "phone": "+1-512-555-0142",
            "address": "123 Maple St, Austin, TX 78701, US",
        },
        "CUST-5002": {
            "name": "Michael Johnson",
            "email": "m.johnson@example.com",
            "phone": "+1-303-555-0178",
            "address": "45 Oak Ave, Denver, CO 80203, US",
        },
        "CUST-5003": {
            "name": "Sofia Martinez",
            "email": "sofia.martinez@example.com",
            "phone": "+1-305-555-0119",
            "address": "78 Pine Rd, Miami, FL 33101, US",
        },
    }

    return list_of_customers

@app.get("/get-customers/{customer}")
def get_customer(customer):
    list_of_customers = {
        "CUST-5001": {
            "name": "Emily Carter",
            "email": "emily.carter@example.com",
            "phone": "+1-512-555-0142",
            "address": "123 Maple St, Austin, TX 78701, US",
        },
        "CUST-5002": {
            "name": "Michael Johnson",
            "email": "m.johnson@example.com",
            "phone": "+1-303-555-0178",
            "address": "45 Oak Ave, Denver, CO 80203, US",
        },
        "CUST-5003": {
            "name": "Sofia Martinez",
            "email": "sofia.martinez@example.com",
            "phone": "+1-305-555-0119",
            "address": "78 Pine Rd, Miami, FL 33101, US",
        },
    }

    if customer not in list_of_customers:
        raise HTTPException(status_code=404, detail="Customer not found")

    return list_of_customers[customer]


@app.post("/add-id/{id}")
def add_id(id):
    # Need to do a curl post: curl -X POST http://127.0.0.1:8000/add-id/300
    customer = {
        "CUST-5001": {
            "name": "Emily Carter",
            "email": "emily.carter@example.com",
            "phone": "+1-512-555-0142",
            "address": "123 Maple St, Austin, TX 78701, US",
            "id": ""
        }
    }

    customer["CUST-5001"]["id"] = id
    return customer



