from prometheus_client import Counter, Histogram, Gauge

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

ORDERS_TOTAL = Counter(
    "orders_total",
    "Total orders placed",
)

ORDERS_PROCESSING_SECONDS = Histogram(
    "orders_processing_seconds",
    "Order processing time in seconds",
)

PRODUCTS_IN_STOCK = Gauge(
    "products_in_stock",
    "Number of products currently in stock",
)

MEMORY_LEAK_BYTES = Gauge(
    "memory_leak_bytes",
    "Bytes consumed by simulated memory leak",
)
