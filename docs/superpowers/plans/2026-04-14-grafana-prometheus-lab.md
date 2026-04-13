# Grafana + Prometheus + Loki Learning Lab — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Docker-based learning lab with a FastAPI app, Prometheus, Loki, Promtail, Grafana, and node-exporter, plus 24 practical scenarios in Polish for learning monitoring from scratch.

**Architecture:** Single `docker-compose.yml` brings up the full stack. A FastAPI "shop API" generates metrics and structured JSON logs. Prometheus scrapes metrics, Promtail ships logs to Loki, Grafana visualizes both. Simulation endpoints (`/simulate/*`) allow triggering problems for break & fix scenarios.

**Tech Stack:** Python 3.12 / FastAPI / structlog / prometheus-client, Docker Compose, Prometheus, Loki, Promtail, Grafana, node-exporter

---

## File Structure

```
grafana-prometheus-lab/
├── .gitignore
├── docker-compose.yml
├── README.md
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── metrics.py
│   ├── simulate.py
│   └── logging_config.py
├── prometheus/
│   ├── prometheus.yml
│   └── alert_rules.yml
├── loki/
│   └── loki-config.yml
├── promtail/
│   └── promtail-config.yml
├── grafana/
│   ├── grafana.ini
│   └── provisioning/
│       ├── datasources/
│       │   └── datasources.yml
│       └── dashboards/
│           ├── dashboards.yml
│           └── starter.json
├── scenarios/
│   ├── README.md
│   ├── 01-prometheus/
│   │   ├── 01-targets.md
│   │   ├── 02-first-promql.md
│   │   ├── 03-rate-and-counter.md
│   │   ├── 04-histogram-percentiles.md
│   │   └── 05-label-filtering.md
│   ├── 02-grafana-dashboards/
│   │   ├── 06-first-panel.md
│   │   ├── 07-application-overview.md
│   │   ├── 08-variables.md
│   │   ├── 09-gauge-stat.md
│   │   └── 10-annotations.md
│   ├── 03-loki-logs/
│   │   ├── 11-explore.md
│   │   ├── 12-logql-filtering.md
│   │   ├── 13-logql-parsing.md
│   │   ├── 14-logs-dashboard.md
│   │   └── 15-correlation.md
│   ├── 04-alerts/
│   │   ├── 16-first-alert.md
│   │   ├── 17-latency-alert.md
│   │   ├── 18-log-alert.md
│   │   └── 19-contact-points.md
│   └── 05-break-and-fix/
│       ├── 20-slow-endpoint.md
│       ├── 21-error-storm.md
│       ├── 22-memory-leak.md
│       ├── 23-full-diagnosis.md
│       └── 24-oncall-dashboard.md
└── scripts/
    └── generate_traffic.sh
```

---

### Task 1: Project scaffolding

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Initialize git repository**

```bash
cd /home/kkopec/projects/grafana-prometheus-lab
git init
```

- [ ] **Step 2: Create .gitignore**

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
.venv/
*.egg-info/

# Environment
.env

# IDE
.vscode/
.idea/

# Docker volumes data
grafana-data/
prometheus-data/
loki-data/
```

- [ ] **Step 3: Create directory structure**

```bash
mkdir -p app
mkdir -p prometheus
mkdir -p loki
mkdir -p promtail
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
mkdir -p scenarios/01-prometheus
mkdir -p scenarios/02-grafana-dashboards
mkdir -p scenarios/03-loki-logs
mkdir -p scenarios/04-alerts
mkdir -p scenarios/05-break-and-fix
mkdir -p scripts
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore: initialize project with .gitignore"
```

---

### Task 2: FastAPI app — requirements.txt and Dockerfile

**Files:**
- Create: `app/requirements.txt`
- Create: `app/Dockerfile`

- [ ] **Step 1: Create requirements.txt**

```txt
fastapi==0.115.6
uvicorn==0.34.0
prometheus-client==0.21.1
structlog==24.4.0
```

- [ ] **Step 2: Create Dockerfile**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 3: Commit**

```bash
git add app/requirements.txt app/Dockerfile
git commit -m "feat(app): add requirements and Dockerfile"
```

---

### Task 3: FastAPI app — logging_config.py

**Files:**
- Create: `app/logging_config.py`

- [ ] **Step 1: Create logging_config.py**

```python
import logging
import structlog


def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )
```

- [ ] **Step 2: Commit**

```bash
git add app/logging_config.py
git commit -m "feat(app): add structured JSON logging config"
```

---

### Task 4: FastAPI app — metrics.py

**Files:**
- Create: `app/metrics.py`

- [ ] **Step 1: Create metrics.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add app/metrics.py
git commit -m "feat(app): add Prometheus metric definitions"
```

---

### Task 5: FastAPI app — simulate.py

**Files:**
- Create: `app/simulate.py`

- [ ] **Step 1: Create simulate.py**

```python
from dataclasses import dataclass, field

from fastapi import APIRouter

router = APIRouter(prefix="/simulate", tags=["simulation"])


@dataclass
class SimulationState:
    slow_enabled: bool = False
    errors_enabled: bool = False
    memory_leak_enabled: bool = False
    _leak_store: list = field(default_factory=list)


simulation_state = SimulationState()


@router.post("/slow")
async def toggle_slow():
    simulation_state.slow_enabled = not simulation_state.slow_enabled
    return {"slow_enabled": simulation_state.slow_enabled}


@router.post("/errors")
async def toggle_errors():
    simulation_state.errors_enabled = not simulation_state.errors_enabled
    return {"errors_enabled": simulation_state.errors_enabled}


@router.post("/memory-leak")
async def toggle_memory_leak():
    simulation_state.memory_leak_enabled = not simulation_state.memory_leak_enabled
    if not simulation_state.memory_leak_enabled:
        simulation_state._leak_store.clear()
    return {"memory_leak_enabled": simulation_state.memory_leak_enabled}


@router.post("/reset")
async def reset_all():
    simulation_state.slow_enabled = False
    simulation_state.errors_enabled = False
    simulation_state.memory_leak_enabled = False
    simulation_state._leak_store.clear()
    return {"status": "all simulations reset"}


@router.get("/status")
async def get_status():
    return {
        "slow_enabled": simulation_state.slow_enabled,
        "errors_enabled": simulation_state.errors_enabled,
        "memory_leak_enabled": simulation_state.memory_leak_enabled,
        "leak_size_mb": round(len(simulation_state._leak_store) * 102400 / 1024 / 1024, 2),
    }
```

- [ ] **Step 2: Commit**

```bash
git add app/simulate.py
git commit -m "feat(app): add simulation endpoints for break-and-fix scenarios"
```

---

### Task 6: FastAPI app — main.py

**Files:**
- Create: `app/main.py`

- [ ] **Step 1: Create main.py**

```python
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
```

- [ ] **Step 2: Verify app builds**

```bash
cd /home/kkopec/projects/grafana-prometheus-lab
docker build -t shop-api-test ./app
```

Expected: image builds successfully.

- [ ] **Step 3: Commit**

```bash
git add app/main.py
git commit -m "feat(app): add main FastAPI application with endpoints and middleware"
```

---

### Task 7: Prometheus configuration

**Files:**
- Create: `prometheus/prometheus.yml`
- Create: `prometheus/alert_rules.yml`

- [ ] **Step 1: Create prometheus.yml**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "fastapi-app"
    static_configs:
      - targets: ["app:8000"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]
```

- [ ] **Step 2: Create alert_rules.yml**

```yaml
groups:
  - name: app_alerts
    rules:
      - alert: HighErrorRate
        expr: >
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m]))
          > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Error rate powyżej 10%"

      - alert: HighLatency
        expr: >
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency powyżej 1s"
```

- [ ] **Step 3: Commit**

```bash
git add prometheus/
git commit -m "feat(prometheus): add scrape config and alert rules"
```

---

### Task 8: Loki and Promtail configuration

**Files:**
- Create: `loki/loki-config.yml`
- Create: `promtail/promtail-config.yml`

- [ ] **Step 1: Create loki-config.yml**

```yaml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2020-10-24
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

limits_config:
  allow_structured_metadata: true
  volume_enabled: true
```

- [ ] **Step 2: Create promtail-config.yml**

```yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ["__meta_docker_container_name"]
        regex: "/(.*)"
        target_label: "container"
      - source_labels: ["__meta_docker_container_log_stream"]
        target_label: "logstream"
      - source_labels: ["__meta_docker_container_label_com_docker_compose_service"]
        target_label: "service"
```

- [ ] **Step 3: Commit**

```bash
git add loki/ promtail/
git commit -m "feat(loki): add Loki and Promtail configuration"
```

---

### Task 9: Grafana configuration and provisioning

**Files:**
- Create: `grafana/grafana.ini`
- Create: `grafana/provisioning/datasources/datasources.yml`
- Create: `grafana/provisioning/dashboards/dashboards.yml`
- Create: `grafana/provisioning/dashboards/starter.json`

- [ ] **Step 1: Create grafana.ini**

```ini
[auth.anonymous]
enabled = true
org_role = Admin

[auth]
disable_login_form = true
```

- [ ] **Step 2: Create datasources.yml**

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    uid: prometheus

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    uid: loki
```

- [ ] **Step 3: Create dashboards.yml**

```yaml
apiVersion: 1

providers:
  - name: "default"
    orgId: 1
    folder: ""
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

- [ ] **Step 4: Create starter.json**

```json
{
  "annotations": {
    "list": []
  },
  "editable": true,
  "graphTooltip": 1,
  "panels": [
    {
      "id": 1,
      "type": "timeseries",
      "title": "Requests per Second",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[1m])) by (endpoint)",
          "legendFormat": "{{ endpoint }}"
        }
      ],
      "fieldConfig": {
        "defaults": { "unit": "reqps" },
        "overrides": []
      }
    },
    {
      "id": 2,
      "type": "stat",
      "title": "Error Rate",
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 0 },
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 5 },
              { "color": "red", "value": 10 }
            ]
          }
        },
        "overrides": []
      }
    },
    {
      "id": 3,
      "type": "timeseries",
      "title": "Request Duration (p95)",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 8 },
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
          "legendFormat": "p95"
        }
      ],
      "fieldConfig": {
        "defaults": { "unit": "s" },
        "overrides": []
      }
    },
    {
      "id": 4,
      "type": "gauge",
      "title": "Products in Stock",
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 8 },
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "targets": [
        {
          "expr": "products_in_stock"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "red", "value": null },
              { "color": "yellow", "value": 50 },
              { "color": "green", "value": 100 }
            ]
          }
        },
        "overrides": []
      }
    }
  ],
  "refresh": "10s",
  "schemaVersion": 39,
  "tags": ["fastapi", "monitoring"],
  "templating": { "list": [] },
  "time": { "from": "now-30m", "to": "now" },
  "title": "FastAPI App - Starter",
  "uid": "fastapi-starter"
}
```

- [ ] **Step 5: Commit**

```bash
git add grafana/
git commit -m "feat(grafana): add config, datasource provisioning, and starter dashboard"
```

---

### Task 10: Docker Compose

**Files:**
- Create: `docker-compose.yml`

- [ ] **Step 1: Create docker-compose.yml**

```yaml
services:
  app:
    build: ./app
    ports:
      - "8000:8000"
    depends_on:
      - prometheus
    labels:
      - "com.docker-compose.service=app"

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./prometheus/alert_rules.yml:/etc/prometheus/alert_rules.yml:ro

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./loki/loki-config.yml:/etc/loki/loki-config.yml:ro
    command: -config.file=/etc/loki/loki-config.yml

  promtail:
    image: grafana/promtail:latest
    volumes:
      - ./promtail/promtail-config.yml:/etc/promtail/promtail-config.yml:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: -config.file=/etc/promtail/promtail-config.yml
    depends_on:
      - loki

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/grafana.ini:/etc/grafana/grafana.ini:ro
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/provisioning/dashboards/starter.json:/var/lib/grafana/dashboards/starter.json:ro
    depends_on:
      - prometheus
      - loki

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
```

- [ ] **Step 2: Commit**

```bash
git add docker-compose.yml
git commit -m "feat: add docker-compose with full monitoring stack"
```

---

### Task 11: Traffic generator script

**Files:**
- Create: `scripts/generate_traffic.sh`

- [ ] **Step 1: Create generate_traffic.sh**

```bash
#!/bin/bash
# Skrypt generujący ruch do aplikacji FastAPI.
# Użycie: ./scripts/generate_traffic.sh
# Zatrzymanie: Ctrl+C

BASE_URL="http://localhost:8000"

echo "Generowanie ruchu do $BASE_URL ..."
echo "Naciśnij Ctrl+C aby zatrzymać."
echo ""

while true; do
    # Lista produktów
    curl -s "$BASE_URL/products" > /dev/null

    # Szczegóły produktu (id 1-7, gdzie 6-7 dadzą 404)
    PRODUCT_ID=$((RANDOM % 7 + 1))
    curl -s "$BASE_URL/products/$PRODUCT_ID" > /dev/null

    # Zamówienie (co 3. iteracja)
    if [ $((RANDOM % 3)) -eq 0 ]; then
        curl -s -X POST "$BASE_URL/orders" \
            -H "Content-Type: application/json" \
            -d "{\"product_id\": $((RANDOM % 5 + 1)), \"quantity\": $((RANDOM % 3 + 1))}" > /dev/null
    fi

    # Healthcheck (co 5. iteracja)
    if [ $((RANDOM % 5)) -eq 0 ]; then
        curl -s "$BASE_URL/health" > /dev/null
    fi

    # Losowy odstęp 0.1-0.5s
    sleep 0.$((RANDOM % 5 + 1))
done
```

- [ ] **Step 2: Make executable and commit**

```bash
chmod +x scripts/generate_traffic.sh
git add scripts/
git commit -m "feat: add traffic generator script"
```

---

### Task 12: Stack verification

- [ ] **Step 1: Start the stack**

```bash
cd /home/kkopec/projects/grafana-prometheus-lab
docker compose up -d --build
```

- [ ] **Step 2: Wait for services and verify**

```bash
sleep 10
docker compose ps
```

Expected: all 6 services running (app, prometheus, loki, promtail, grafana, node-exporter).

- [ ] **Step 3: Test FastAPI endpoints**

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8000/products
curl -s http://localhost:8000/products/1
curl -s -X POST http://localhost:8000/orders -H "Content-Type: application/json" -d '{"product_id": 1, "quantity": 2}'
curl -s http://localhost:8000/metrics | head -20
```

Expected: JSON responses from each endpoint, raw Prometheus metrics from `/metrics`.

- [ ] **Step 4: Test Prometheus**

```bash
curl -s http://localhost:9090/api/v1/targets | python3 -m json.tool | head -30
```

Expected: targets listed with status "up".

- [ ] **Step 5: Test Grafana**

```bash
curl -s http://localhost:3000/api/health
curl -s http://localhost:3000/api/datasources | python3 -m json.tool
```

Expected: Grafana healthy, two datasources (Prometheus, Loki) listed.

- [ ] **Step 6: Tear down**

```bash
docker compose down
```

---

### Task 13: Project README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README.md**

```markdown
# Grafana + Prometheus + Loki — Learning Lab

Praktyczne środowisko do nauki monitoringu aplikacji. Stawiasz stack jednym poleceniem, a potem rozwiązujesz 24 scenariusze — od pierwszego zapytania PromQL po diagnozowanie symulowanych awarii.

## Wymagania

- Docker i Docker Compose
- curl (do generowania ruchu)
- Przeglądarka (Grafana UI, Prometheus UI)

## Szybki start

```bash
# 1. Uruchom stack
docker compose up -d --build

# 2. Wygeneruj ruch (w osobnym terminalu)
./scripts/generate_traffic.sh

# 3. Otwórz w przeglądarce
#    Grafana:    http://localhost:3000
#    Prometheus: http://localhost:9090
#    FastAPI:    http://localhost:8000/docs
```

## Adresy usług

| Usługa | URL | Opis |
|--------|-----|------|
| Grafana | http://localhost:3000 | Dashboardy, Explore, Alerty |
| Prometheus | http://localhost:9090 | Metryki, PromQL, Targets |
| FastAPI App | http://localhost:8000 | Aplikacja sklepu |
| FastAPI Docs | http://localhost:8000/docs | Swagger UI |
| Loki | http://localhost:3100 | API logów (używane przez Grafanę) |
| Node Exporter | http://localhost:9100 | Metryki systemowe |

## Scenariusze

| # | Rozdział | Tematyka |
|---|----------|----------|
| 1-5 | Prometheus | Targets, PromQL, rate, histogram, labele |
| 6-10 | Grafana Dashboardy | Panele, dashboardy, zmienne, adnotacje |
| 11-15 | Loki & Logi | LogQL, filtrowanie, parsowanie, korelacja |
| 16-19 | Alerty | Error rate, latency, logi, contact points |
| 20-24 | Break & Fix | Wolne endpointy, błędy 500, memory leak, diagnoza |

Szczegóły: [scenarios/README.md](scenarios/README.md)

## Symulacje awarii (Break & Fix)

Aplikacja ma wbudowane endpointy do symulacji problemów:

```bash
# Włącz losowe opóźnienia
curl -X POST http://localhost:8000/simulate/slow

# Włącz losowe błędy 500
curl -X POST http://localhost:8000/simulate/errors

# Włącz wyciek pamięci
curl -X POST http://localhost:8000/simulate/memory-leak

# Sprawdź stan symulacji
curl http://localhost:8000/simulate/status

# Zresetuj wszystko
curl -X POST http://localhost:8000/simulate/reset
```

## Lokalne środowisko (opcjonalnie)

Dla wsparcia IDE (autocompletion, linting):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
```

## Zatrzymanie

```bash
docker compose down
```
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add project README with quickstart and scenario overview"
```

---

### Task 14: Scenarios — README + Chapter 1 (Prometheus)

**Files:**
- Create: `scenarios/README.md`
- Create: `scenarios/01-prometheus/01-targets.md`
- Create: `scenarios/01-prometheus/02-first-promql.md`
- Create: `scenarios/01-prometheus/03-rate-and-counter.md`
- Create: `scenarios/01-prometheus/04-histogram-percentiles.md`
- Create: `scenarios/01-prometheus/05-label-filtering.md`

- [ ] **Step 1: Create scenarios/README.md**

```markdown
# Scenariusze

## Jak korzystać

1. Uruchom stack: `docker compose up -d --build`
2. Uruchom generator ruchu: `./scripts/generate_traffic.sh`
3. Otwórz scenariusz i wykonuj zadania
4. Gdy utkniesz — rozwiń podpowiedzi
5. Gdy chcesz sprawdzić odpowiedź — rozwiń rozwiązanie

Poczekaj 2-3 minuty po uruchomieniu stacku, żeby metryki i logi się zebrały.

## Spis treści

### Rozdział 1: Prometheus — metryki i PromQL
1. [Poznaj targety](01-prometheus/01-targets.md)
2. [Pierwsze zapytanie PromQL](01-prometheus/02-first-promql.md)
3. [Rate i Counter](01-prometheus/03-rate-and-counter.md)
4. [Histogram i percentyle](01-prometheus/04-histogram-percentiles.md)
5. [Filtrowanie labelami](01-prometheus/05-label-filtering.md)

### Rozdział 2: Grafana — dashboardy
6. [Pierwszy panel](02-grafana-dashboards/06-first-panel.md)
7. [Dashboard "Application Overview"](02-grafana-dashboards/07-application-overview.md)
8. [Zmienne (variables)](02-grafana-dashboards/08-variables.md)
9. [Gauge i Stat panele](02-grafana-dashboards/09-gauge-stat.md)
10. [Adnotacje](02-grafana-dashboards/10-annotations.md)

### Rozdział 3: Loki — logi i LogQL
11. [Explore w Grafanie](03-loki-logs/11-explore.md)
12. [LogQL — filtrowanie](03-loki-logs/12-logql-filtering.md)
13. [LogQL — parsowanie](03-loki-logs/13-logql-parsing.md)
14. [Dashboard z logami](03-loki-logs/14-logs-dashboard.md)
15. [Korelacja logi i metryki](03-loki-logs/15-correlation.md)

### Rozdział 4: Alerty
16. [Pierwszy alert](04-alerts/16-first-alert.md)
17. [Alert na latency](04-alerts/17-latency-alert.md)
18. [Alert na logi](04-alerts/18-log-alert.md)
19. [Contact points i silence](04-alerts/19-contact-points.md)

### Rozdział 5: Break & Fix
20. [Wolny endpoint](05-break-and-fix/20-slow-endpoint.md)
21. [Fala błędów 500](05-break-and-fix/21-error-storm.md)
22. [Wyciek pamięci](05-break-and-fix/22-memory-leak.md)
23. [Pełna diagnoza](05-break-and-fix/23-full-diagnosis.md)
24. [Dashboard On-Call](05-break-and-fix/24-oncall-dashboard.md)
```

- [ ] **Step 2: Create 01-targets.md**

```markdown
# Scenariusz 1: Poznaj targety

## Cel
Zrozumieć czym są targety w Prometheus i jak sprawdzić, czy zbieranie metryk działa.

## Kontekst
Prometheus działa w modelu **pull** — co określony czas (domyślnie 15s) odpytuje skonfigurowane endpointy (`/metrics`) i zapisuje pobrane metryki. Każdy taki endpoint to **target**. Jeśli target ma status UP, oznacza to, że Prometheus poprawnie pobiera z niego metryki.

## Zadanie
1. Otwórz Prometheus UI: http://localhost:9090
2. Przejdź do **Status → Targets**
3. Odpowiedz na pytania:
   - Ile targetów jest skonfigurowanych?
   - Jakie to targety (nazwy jobów)?
   - Co oznacza status **UP**?
   - Jaki jest interwał scrapowania (scrape interval)?

<details>
<summary>Podpowiedź 1</summary>

Strona Targets pokazuje tabelę z kolumnami: Endpoint, State, Labels, Last Scrape, Scrape Duration, Error.

</details>

<details>
<summary>Podpowiedź 2</summary>

Nazwy jobów odpowiadają sekcjom `job_name` w pliku `prometheus/prometheus.yml`.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**3 targety:**

| Job | Target | Opis |
|-----|--------|------|
| `prometheus` | `localhost:9090` | Sam Prometheus monitoruje siebie |
| `fastapi-app` | `app:8000` | Nasza aplikacja sklepu |
| `node-exporter` | `node-exporter:9100` | Metryki systemowe hosta |

- **UP** oznacza, że Prometheus może się połączyć z targetem i pobrać metryki
- **Scrape interval** to 15s (ustawione w `global.scrape_interval` w `prometheus.yml`)

Warto też kliknąć na endpoint targetu (np. `http://app:8000/metrics`) — zobaczysz surowe metryki w formacie tekstowym Prometheus.

</details>
```

- [ ] **Step 3: Create 02-first-promql.md**

```markdown
# Scenariusz 2: Pierwsze zapytanie PromQL

## Cel
Nauczyć się wykonywać podstawowe zapytania PromQL i rozumieć wynik.

## Kontekst
**PromQL** (Prometheus Query Language) to język zapytań Prometheus. Każda metryka ma nazwę i zestaw **labeli** (etykiet) w formacie `nazwa{label1="val1", label2="val2"}`. Każda unikalna kombinacja nazwy i labeli to osobna **seria czasowa** (time series).

## Zadanie
1. Otwórz Prometheus UI: http://localhost:9090
2. W polu zapytania wpisz: `http_requests_total`
3. Kliknij **Execute**
4. Przełącz na zakładkę **Table** i **Graph**
5. Odpowiedz:
   - Ile serii czasowych widzisz?
   - Jakie labele mają te serie?
   - Dlaczego jest ich kilka, a nie jedna?

<details>
<summary>Podpowiedź 1</summary>

Każda unikalna kombinacja `method` + `endpoint` + `status` tworzy osobną serię. Np. `GET /products 200` i `GET /products 500` to dwie różne serie.

</details>

<details>
<summary>Podpowiedź 2</summary>

Spróbuj kliknąć na konkretną serię w tabeli — zobaczysz jej pełną nazwę z labelami.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

Zobaczysz wiele serii czasowych, np.:

```
http_requests_total{endpoint="/products", method="GET", status="200"} → 142
http_requests_total{endpoint="/products/1", method="GET", status="200"} → 87
http_requests_total{endpoint="/products/6", method="GET", status="404"} → 23
http_requests_total{endpoint="/orders", method="POST", status="200"} → 45
```

- **Labele:** `method` (GET/POST), `endpoint` (ścieżka URL), `status` (kod HTTP)
- Jest wiele serii, bo każda kombinacja labeli = osobna seria
- Wartość to **counter** — rośnie monotonnie, nigdy nie maleje (reset tylko przy restarcie)

W zakładce **Graph** widzisz jak counter rośnie w czasie — to jeszcze nie jest "ile requestów na sekundę", to surowa suma.

</details>
```

- [ ] **Step 4: Create 03-rate-and-counter.md**

```markdown
# Scenariusz 3: Rate i Counter

## Cel
Zrozumieć dlaczego nie czytamy counterów bezpośrednio i jak używać `rate()` do obliczania tempa zmian.

## Kontekst
Counter to metryka, która tylko rośnie. Surowa wartość (np. 14523) mówi nam niewiele — zależy od tego kiedy aplikacja wystartowała. Funkcja `rate()` oblicza **średnią zmianę na sekundę** w zadanym oknie czasowym. Np. `rate(metryka[5m])` = ile razy średnio na sekundę metryka rosła w ostatnich 5 minutach.

## Zadanie
1. W Prometheus UI wpisz: `rate(http_requests_total[5m])`
2. Przełącz na **Graph** — widzisz RPS (requests per second) dla każdej serii
3. Teraz oblicz łączne RPS (suma ze wszystkich serii): `sum(rate(http_requests_total[5m]))`
4. Porównaj wyniki z różnymi oknami: `[1m]`, `[5m]`, `[15m]`
5. Co się zmienia?

<details>
<summary>Podpowiedź 1</summary>

Krótsze okno (1m) daje bardziej "nerwowy" wykres, ale reaguje szybciej na zmiany. Dłuższe okno (15m) wygładza wykres, ale opóźnia reakcję.

</details>

<details>
<summary>Podpowiedź 2</summary>

`sum()` sumuje wszystkie serie. Możesz też sumować po konkretnym labelu: `sum by (endpoint)(rate(http_requests_total[5m]))` — RPS per endpoint.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

```promql
# RPS per seria (każda kombinacja method/endpoint/status)
rate(http_requests_total[5m])

# Łączne RPS
sum(rate(http_requests_total[5m]))

# RPS per endpoint
sum by (endpoint)(rate(http_requests_total[5m]))

# RPS per status code
sum by (status)(rate(http_requests_total[5m]))
```

**Różnice między oknami:**
- `[1m]` — szybko reaguje na zmiany, ale "skacze"
- `[5m]` — dobry balans (najczęściej używany)
- `[15m]` — gładki wykres, ale opóźniony

**Zasada:** `rate()` to najważniejsza funkcja w PromQL. Prawie nigdy nie czytamy counterów bezpośrednio.

</details>
```

- [ ] **Step 5: Create 04-histogram-percentiles.md**

```markdown
# Scenariusz 4: Histogram i percentyle

## Cel
Zrozumieć jak działają histogramy w Prometheus i jak obliczać percentyle latency.

## Kontekst
Histogram w Prometheus to tak naprawdę 3 metryki:
- `_bucket{le="X"}` — ile requestów trwało ≤ X sekund (counter per bucket)
- `_count` — łączna liczba obserwacji
- `_sum` — suma wszystkich wartości

Funkcja `histogram_quantile()` oblicza przybliżony percentyl na podstawie bucketów.

## Zadanie
1. Sprawdź surowe buckety: `http_request_duration_seconds_bucket`
2. Oblicz **medianę** (p50) czasu odpowiedzi: `histogram_quantile(0.5, rate(http_request_duration_seconds_bucket[5m]))`
3. Oblicz **p95**: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`
4. Oblicz **p99**: zamień `0.95` na `0.99`
5. Porównaj p50, p95, p99 na wykresie — dlaczego się różnią?
6. Sprawdź osobno endpoint `/orders`: dodaj filtr `{endpoint="/orders"}`

<details>
<summary>Podpowiedź 1</summary>

W bucketach `le` oznacza "less or equal". Bucket `le="0.1"` liczy ile requestów trwało ≤ 100ms. Zawsze jest bucket `le="+Inf"` (wszystkie requesty).

</details>

<details>
<summary>Podpowiedź 2</summary>

Aby histogram_quantile działał per endpoint, musisz użyć `by (le, endpoint)` w `rate()`:

```promql
histogram_quantile(0.95, sum by (le, endpoint)(rate(http_request_duration_seconds_bucket[5m])))
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

```promql
# Mediana (50% requestów jest szybszych od tej wartości)
histogram_quantile(0.5, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# p95 (95% requestów jest szybszych)
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# p99
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# p95 per endpoint
histogram_quantile(0.95, sum by (le, endpoint)(rate(http_request_duration_seconds_bucket[5m])))
```

**Dlaczego się różnią?**
- p50 (mediana) — typowy request
- p95 — najwolniejsze 5% requestów. To jest wartość, którą monitorujemy w praktyce
- p99 — najwolniejszy 1%. Ważne dla SLA/SLO

Endpoint `/orders` jest wolniejszy (ma `asyncio.sleep`) — jego p95 powinien być wyższy niż `/products`.

</details>
```

- [ ] **Step 6: Create 05-label-filtering.md**

```markdown
# Scenariusz 5: Filtrowanie labelami

## Cel
Nauczyć się filtrować metryki po labelach i obliczyć error rate.

## Kontekst
PromQL wspiera 4 operatory dopasowania labeli:
- `=` — dokładne dopasowanie
- `!=` — nierówne
- `=~` — regex match
- `!~` — regex not match

Error rate to procent requestów zakończonych błędem (status 5xx) w stosunku do wszystkich requestów.

## Zadanie
1. Znajdź requesty tylko do endpointu `/products`: `http_requests_total{endpoint="/products"}`
2. Znajdź requesty z błędami (status 5xx): `http_requests_total{status=~"5.."}`
3. Znajdź requesty zakończone powodzeniem (nie-5xx): `http_requests_total{status!~"5.."}`
4. Oblicz **error rate** (procentowo): podziel rate błędów przez rate wszystkich requestów
5. Oblicz error rate **per endpoint**

<details>
<summary>Podpowiedź 1</summary>

`status=~"5.."` to regex — `5` + dowolne 2 znaki. Dopasowuje 500, 501, 502 itd.

</details>

<details>
<summary>Podpowiedź 2</summary>

Error rate = `rate(błędy) / rate(wszystkie)`. Użyj `sum()` żeby zagregować serie:

```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

```promql
# Tylko endpoint /products
http_requests_total{endpoint="/products"}

# Tylko błędy 5xx
http_requests_total{status=~"5.."}

# Error rate (0-1, gdzie 0.1 = 10%)
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# Error rate w procentach
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
* 100

# Error rate per endpoint
sum by (endpoint)(rate(http_requests_total{status=~"5.."}[5m]))
/
sum by (endpoint)(rate(http_requests_total[5m]))
* 100
```

**Wskazówka:** Jeśli error rate = 0 (brak błędów), uruchom symulację: `curl -X POST http://localhost:8000/simulate/errors`, poczekaj minutę i sprawdź ponownie. Potem zresetuj: `curl -X POST http://localhost:8000/simulate/reset`.

</details>
```

- [ ] **Step 7: Commit**

```bash
git add scenarios/README.md scenarios/01-prometheus/
git commit -m "docs: add scenarios README and Chapter 1 (Prometheus & PromQL)"
```

---

### Task 15: Scenarios — Chapter 2 (Grafana Dashboards)

**Files:**
- Create: `scenarios/02-grafana-dashboards/06-first-panel.md`
- Create: `scenarios/02-grafana-dashboards/07-application-overview.md`
- Create: `scenarios/02-grafana-dashboards/08-variables.md`
- Create: `scenarios/02-grafana-dashboards/09-gauge-stat.md`
- Create: `scenarios/02-grafana-dashboards/10-annotations.md`

- [ ] **Step 1: Create 06-first-panel.md**

```markdown
# Scenariusz 6: Pierwszy panel

## Cel
Stworzyć pierwszy panel w Grafanie — wykres RPS w czasie.

## Kontekst
Grafana wizualizuje dane z Prometheusa jako **panele** w **dashboardach**. Panel to pojedynczy wykres/statystyka. Dashboard to zbiór paneli. Prometheus dostarczył dane, teraz trzeba je ładnie pokazać.

## Zadanie
1. Otwórz Grafanę: http://localhost:3000
2. Kliknij **+ → New dashboard → Add visualization**
3. Wybierz datasource **Prometheus**
4. W polu **Metric** wpisz zapytanie: `sum(rate(http_requests_total[1m])) by (endpoint)`
5. W polu **Legend** wpisz: `{{ endpoint }}`
6. Ustaw tytuł panelu: "Requests per Second"
7. Kliknij **Apply**
8. Zapisz dashboard jako "Mój pierwszy dashboard"

<details>
<summary>Podpowiedź 1</summary>

Pole metryki znajdziesz na dole panelu edycji. Przełącz z "Builder" na "Code" jeśli chcesz wpisać PromQL ręcznie.

</details>

<details>
<summary>Podpowiedź 2</summary>

`{{ endpoint }}` w Legend to szablon — Grafana zamieni go na wartość labela `endpoint` z każdej serii.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

1. **Dashboards → New → New dashboard → Add visualization**
2. Datasource: **Prometheus**
3. Przełącz na tryb **Code** (prawy górny róg edytora zapytań)
4. Wpisz: `sum(rate(http_requests_total[1m])) by (endpoint)`
5. Poniżej w **Options → Legend**: `{{ endpoint }}`
6. W prawym panelu u góry — wpisz tytuł: **Requests per Second**
7. Kliknij **Apply** (prawy górny róg)
8. Kliknij ikonę dyskietki (💾) → nazwa: "Mój pierwszy dashboard" → **Save**

Powinieneś widzieć wykres liniowy z osobną linią dla każdego endpointu.

</details>
```

- [ ] **Step 2: Create 07-application-overview.md**

```markdown
# Scenariusz 7: Dashboard "Application Overview"

## Cel
Zbudować kompletny dashboard z 4 panelami dający ogólny obraz zdrowia aplikacji.

## Kontekst
Dobry dashboard odpowiada na pytanie "czy aplikacja działa dobrze?" jednym rzutem oka. Kluczowe metryki to: RPS (ruch), latency (szybkość), error rate (poprawność), i specyficzne metryki biznesowe.

## Zadanie
Stwórz nowy dashboard "Application Overview" z 4 panelami:

1. **RPS** (Time series) — `sum(rate(http_requests_total[1m])) by (endpoint)`
2. **Latency p95** (Time series) — `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
3. **Error Rate %** (Stat) — `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100`
4. **Status Codes** (Pie chart) — `sum by (status)(increase(http_requests_total[5m]))`

<details>
<summary>Podpowiedź 1</summary>

Typ panelu wybierasz w prawym panelu edycji, dropdown u góry. Dla Pie chart wybierz typ "Pie chart".

</details>

<details>
<summary>Podpowiedź 2</summary>

Dla panelu Error Rate (Stat): w zakładce prawej ustaw Unit → Misc → Percent (0-100). Dodaj thresholds: zielony < 5%, żółty 5-10%, czerwony > 10%.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

Utwórz nowy dashboard, dodaj 4 panele:

**Panel 1 — RPS:**
- Typ: Time series
- Query: `sum(rate(http_requests_total[1m])) by (endpoint)`
- Legend: `{{ endpoint }}`
- Unit: requests/sec (reqps)

**Panel 2 — Latency p95:**
- Typ: Time series
- Query: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
- Legend: `p95`
- Unit: seconds (s)

**Panel 3 — Error Rate:**
- Typ: Stat
- Query: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100`
- Unit: Percent (0-100)
- Thresholds: green=0, yellow=5, red=10

**Panel 4 — Status Codes:**
- Typ: Pie chart
- Query: `sum by (status)(increase(http_requests_total[5m]))`
- Legend: `{{ status }}`

Zapisz jako "Application Overview".

</details>
```

- [ ] **Step 3: Create 08-variables.md**

```markdown
# Scenariusz 8: Zmienne (variables)

## Cel
Dodać interaktywny dropdown do dashboardu, który filtruje dane po endpoincie.

## Kontekst
Zmienne (template variables) w Grafanie pozwalają na tworzenie dynamicznych dashboardów. Zamiast tworzyć osobny panel dla każdego endpointu, tworzysz jeden dashboard z dropdownem. Zmienna jest dostępna w zapytaniach jako `$nazwa_zmiennej`.

## Zadanie
1. Otwórz dashboard "Application Overview"
2. Wejdź w ustawienia dashboardu (ikona koła zębatego)
3. Przejdź do zakładki **Variables** → **New variable**
4. Stwórz zmienną `endpoint` typu **Query** z Prometheusa
5. Użyj zmiennej w zapytaniach paneli (dodaj filtr `{endpoint="$endpoint"}`)
6. Sprawdź czy dropdown działa — zmień wartość i obserwuj panele

<details>
<summary>Podpowiedź 1</summary>

Zapytanie dla zmiennej, które zwraca wszystkie wartości labela `endpoint`:

```
label_values(http_requests_total, endpoint)
```

</details>

<details>
<summary>Podpowiedź 2</summary>

Zaznacz opcję "Include All option" żeby mieć możliwość wybrania wszystkich endpointów naraz. Ustaw też "Multi-value" aby móc wybrać kilka.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Tworzenie zmiennej:**
1. Dashboard Settings (⚙️) → Variables → New variable
2. Name: `endpoint`
3. Type: **Query**
4. Data source: **Prometheus**
5. Query: `label_values(http_requests_total, endpoint)`
6. Multi-value: ✅
7. Include All option: ✅
8. Click **Apply** → **Save dashboard**

**Użycie zmiennej w panelu RPS:**
Zmień zapytanie z:
```promql
sum(rate(http_requests_total[1m])) by (endpoint)
```
na:
```promql
sum(rate(http_requests_total{endpoint=~"$endpoint"}[1m])) by (endpoint)
```

Użyj `=~` (regex match) zamiast `=`, bo przy Multi-value Grafana generuje regex `val1|val2|val3`.

Powtórz dla pozostałych paneli.

</details>
```

- [ ] **Step 4: Create 09-gauge-stat.md**

```markdown
# Scenariusz 9: Gauge i Stat panele

## Cel
Stworzyć panele pokazujące pojedyncze wartości — aktualny stan magazynu i uptime aplikacji.

## Kontekst
Nie wszystkie dane najlepiej pokazywać jako wykres w czasie. **Stat** pokazuje jedną dużą liczbę (np. error rate). **Gauge** to "zegar" z kolorową skalą (np. stan magazynu). Oba świetnie nadają się do wartości, które chcesz zobaczyć "na pierwszy rzut oka".

## Zadanie
1. Do dashboardu "Application Overview" dodaj panel **Stat** z uptime aplikacji
   - Metryka: `process_uptime_seconds{job="fastapi-app"}`
   - Unit: seconds (duration)
2. Dodaj panel **Gauge** z liczbą produktów w magazynie
   - Metryka: `products_in_stock`
   - Thresholds: czerwony < 50, żółty 50-100, zielony > 100

<details>
<summary>Podpowiedź 1</summary>

`process_uptime_seconds` to wbudowana metryka z `prometheus_client` — nie musisz jej tworzyć, jest automatycznie eksponowana.

</details>

<details>
<summary>Podpowiedź 2</summary>

Dla panelu Stat z uptime: wybierz Unit → Time → seconds (s). Grafana automatycznie sformatuje na "2h 34m 12s".

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Panel Uptime (Stat):**
- Typ: Stat
- Query: `process_uptime_seconds{job="fastapi-app"}`
- Unit: duration (seconds)
- Tytuł: "App Uptime"

**Panel Products in Stock (Gauge):**
- Typ: Gauge
- Query: `products_in_stock`
- Min: 0, Max: 300
- Thresholds: red=null (default), yellow=50, green=100
- Tytuł: "Products in Stock"

Zapisz dashboard.

</details>
```

- [ ] **Step 5: Create 10-annotations.md**

```markdown
# Scenariusz 10: Adnotacje

## Cel
Dodać adnotacje do dashboardu — wizualne znaczniki na osi czasu pokazujące ważne wydarzenia.

## Kontekst
Adnotacje (annotations) to pionowe linie na wykresach, które oznaczają momenty zdarzeń — np. deploy, restart, zmiana konfiguracji. Pomagają korelować zmiany w metrykach z wydarzeniami. Można je dodawać ręcznie lub automatycznie na podstawie zapytań.

## Zadanie
1. Otwórz dashboard "Application Overview"
2. Dodaj ręczną adnotację: kliknij na wykresie w dowolnym miejscu, wybierz "Add annotation", wpisz "Test deploy"
3. Stwórz automatyczną adnotację na podstawie zmian metryki:
   - Dashboard Settings → Annotations → New annotation query
   - Pokaż momenty gdy error rate przekroczył 5%

<details>
<summary>Podpowiedź 1</summary>

Ręczna adnotacja: kliknij i przytrzymaj na wykresie → pojawi się menu z opcją "Add annotation".

</details>

<details>
<summary>Podpowiedź 2</summary>

Automatyczna adnotacja — to jest bardziej zaawansowane. Użyj datasource Prometheus i zapytania:
```promql
sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) > 0.05
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Ręczna adnotacja:**
1. Na dowolnym panelu typu Time series — kliknij i przytrzymaj na wykresie
2. Pojawi się opcja "Add annotation"
3. Wpisz tekst: "Test deploy" → Save

**Automatyczna adnotacja:**
1. Dashboard Settings (⚙️) → Annotations → New annotation query
2. Name: "High Error Rate"
3. Data source: Prometheus
4. Query: `sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) > 0.05`
5. Color: red
6. Apply → Save dashboard

Aby zobaczyć automatyczną adnotację, uruchom symulację błędów:
```bash
curl -X POST http://localhost:8000/simulate/errors
```
Poczekaj 2-3 minuty, potem zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

</details>
```

- [ ] **Step 6: Commit**

```bash
git add scenarios/02-grafana-dashboards/
git commit -m "docs: add Chapter 2 scenarios (Grafana dashboards)"
```

---

### Task 16: Scenarios — Chapter 3 (Loki & LogQL)

**Files:**
- Create: `scenarios/03-loki-logs/11-explore.md`
- Create: `scenarios/03-loki-logs/12-logql-filtering.md`
- Create: `scenarios/03-loki-logs/13-logql-parsing.md`
- Create: `scenarios/03-loki-logs/14-logs-dashboard.md`
- Create: `scenarios/03-loki-logs/15-correlation.md`

- [ ] **Step 1: Create 11-explore.md**

```markdown
# Scenariusz 11: Explore w Grafanie

## Cel
Znaleźć logi aplikacji w Grafana Explore i nauczyć się podstawowej nawigacji.

## Kontekst
**Loki** to system agregacji logów — odpowiednik Prometheusa, ale dla logów. Loki nie indeksuje treści logów (jak Elasticsearch), tylko ich **labele**. To sprawia, że jest lekki i szybki. Logi przeglądamy przez **Grafana Explore** — tryb ad-hoc do eksplorowania danych.

## Zadanie
1. Otwórz Grafanę: http://localhost:3000
2. Kliknij ikonę kompasu w lewym menu → **Explore**
3. W górnym dropdownie wybierz datasource: **Loki**
4. W polu zapytania wpisz: `{service="app"}`
5. Kliknij **Run query**
6. Spróbuj też: `{service="prometheus"}` i `{service="grafana"}`
7. Odpowiedz: jakie labele mają Twoje logi?

<details>
<summary>Podpowiedź 1</summary>

Label `service` pochodzi z konfiguracji Promtail — mapuje docker-compose service name na label loga.

</details>

<details>
<summary>Podpowiedź 2</summary>

Rozwiń pojedynczy wpis loga klikając na niego. Zobaczysz surową treść (JSON) i wykryte labele.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

Zapytanie `{service="app"}` pokazuje logi z kontenera aplikacji FastAPI. Każdy log to JSON:

```json
{"request_id": "a1b2c3d4", "endpoint": "/products", "event": "products_listed", "level": "info", "timestamp": "2026-04-14T10:23:45.123Z"}
```

**Dostępne labele** (widoczne po rozwinięciu loga):
- `service` — nazwa serwisu z docker-compose (app, prometheus, grafana...)
- `container` — nazwa kontenera Docker
- `logstream` — stdout lub stderr

Logi z `{service="app"}` to strukturalne logi JSON z naszej aplikacji FastAPI (skonfigurowane przez `structlog`).

</details>
```

- [ ] **Step 2: Create 12-logql-filtering.md**

```markdown
# Scenariusz 12: LogQL — filtrowanie

## Cel
Nauczyć się filtrować logi po treści i liczyć je.

## Kontekst
**LogQL** to język zapytań Loki (odpowiednik PromQL dla logów). Zapytanie zaczyna się od **selektora labeli** `{label="value"}`, potem dodaje się **pipeline** — filtry, parsery, formatery. Filtr `|=` szuka tekstu, `|~` szuka regexem, `!=` wyklucza tekst.

## Zadanie
1. Znajdź wszystkie logi z błędami: `{service="app"} |= "error"`
2. Znajdź logi ostrzeżeń: `{service="app"} |= "warning"`
3. Wyklucz logi healthcheck: `{service="app"} != "/health"`
4. Policz ile błędów było w czasie — przełącz na tryb **Metric** (nad polem zapytania) i użyj: `count_over_time({service="app"} |= "error" [1m])`

<details>
<summary>Podpowiedź 1</summary>

`|=` to filtr "contains" — szuka tekstu w treści loga. Wielkość liter ma znaczenie. Użyj `|~ "(?i)error"` dla case-insensitive.

</details>

<details>
<summary>Podpowiedź 2</summary>

Przełącznik "Logs" / "Metric" jest nad polem zapytania w Explore. W trybie Metric, LogQL zwraca liczbę (jak PromQL) zamiast treści logów.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

```logql
# Logi z błędami
{service="app"} |= "error"

# Logi z ostrzeżeniami
{service="app"} |= "warning"

# Bez healthchecków
{service="app"} != "/health"

# Łączenie filtrów — błędy bez healthchecków
{service="app"} |= "error" != "/health"

# Zliczanie błędów per minuta (tryb Metric)
count_over_time({service="app"} |= "error" [1m])

# Rate błędów per sekunda
rate({service="app"} |= "error" [1m])
```

Jeśli nie widzisz błędów, uruchom symulację:
```bash
curl -X POST http://localhost:8000/simulate/errors
```
Poczekaj minutę, potem zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

</details>
```

- [ ] **Step 3: Create 13-logql-parsing.md**

```markdown
# Scenariusz 13: LogQL — parsowanie

## Cel
Wyciągnąć pola z JSON logów i tworzyć metryki z logów.

## Kontekst
Nasze logi to JSON. LogQL potrafi je sparsować operatorem `| json` — każde pole JSON staje się labelem, którego można użyć do filtrowania. To potężne narzędzie: zamiast szukać tekstu "error", możesz filtrować po `level="error"` — precyzyjnie.

## Zadanie
1. Sparsuj JSON logi: `{service="app"} | json`
2. Filtruj po sparsowanym polu: `{service="app"} | json | level="error"`
3. Wyciągnij request_id z błędów: `{service="app"} | json | level="error" | line_format "{{.request_id}} — {{.event}}"`
4. Stwórz metrykę — ile requestów per endpoint (tryb Metric): `sum by (endpoint)(count_over_time({service="app"} | json | endpoint!="" [1m]))`

<details>
<summary>Podpowiedź 1</summary>

Po `| json` masz dostęp do wszystkich pól z JSONa jako labeli. Sprawdź jakie pola są dostępne rozwijając log po sparsowaniu.

</details>

<details>
<summary>Podpowiedź 2</summary>

`| line_format` zmienia format wyświetlanego loga. Używa składni Go templates: `{{.nazwa_pola}}`.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

```logql
# Parsowanie JSON — każde pole staje się labelem
{service="app"} | json

# Filtrowanie po sparsowanym polu level
{service="app"} | json | level="error"

# Tylko określone pola w output
{service="app"} | json | level="error" | line_format "{{.request_id}} — {{.event}}"

# Metryka: requesty per endpoint (Metric mode)
sum by (endpoint)(count_over_time({service="app"} | json | endpoint!="" [1m]))

# Metryka: requesty per level
sum by (level)(count_over_time({service="app"} | json [1m]))
```

`| json` + filtrowanie po labelach to najpotężniejsza kombinacja w LogQL. Pozwala na precyzyjne wyszukiwanie bez skanowania tekstu.

</details>
```

- [ ] **Step 4: Create 14-logs-dashboard.md**

```markdown
# Scenariusz 14: Dashboard z logami

## Cel
Dodać panel z logami do dashboardu obok metryk.

## Kontekst
Grafana pozwala mieszać panele z różnych datasource'ów na jednym dashboardzie. Panel typu **Logs** pokazuje logi z Loki. Umieszczony obok paneli z metrykami (Prometheus) daje pełny obraz: widzisz CO się dzieje (metryki) i DLACZEGO (logi).

## Zadanie
1. Otwórz dashboard "Application Overview"
2. Dodaj nowy panel typu **Logs**
3. Datasource: **Loki**
4. Zapytanie: `{service="app"} | json | level="error"`
5. Ustaw tytuł: "Application Errors"
6. Umieść go pod istniejącymi panelami
7. Użyj split view w Explore — otwórz metryki i logi obok siebie

<details>
<summary>Podpowiedź 1</summary>

Typ panelu "Logs" znajdziesz w dropdownie typów. Wyświetla logi w formie listy z timestampem.

</details>

<details>
<summary>Podpowiedź 2</summary>

Split view w Explore: kliknij przycisk "Split" (prawy górny róg Explore). Lewa strona — Prometheus, prawa — Loki. Oba dzielą ten sam zakres czasu.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Panel Logs na dashboardzie:**
1. Dashboard → Add visualization
2. Datasource: **Loki**
3. Zapytanie (Code mode): `{service="app"} | json | level=~"error|warning"`
4. Typ panelu: **Logs**
5. Tytuł: "Application Errors & Warnings"
6. Apply → przeciągnij panel na dół dashboardu
7. Save dashboard

**Split view w Explore:**
1. Explore (kompas) → datasource: Prometheus
2. Zapytanie: `sum(rate(http_requests_total{status=~"5.."}[1m]))`
3. Kliknij **Split** (prawy górny róg)
4. W prawym panelu: datasource: **Loki**
5. Zapytanie: `{service="app"} | json | level="error"`

Teraz widzisz metryki i logi obok siebie z tym samym zakresem czasu.

</details>
```

- [ ] **Step 5: Create 15-correlation.md**

```markdown
# Scenariusz 15: Korelacja logi i metryki

## Cel
Po zaobserwowaniu anomalii w metrykach, znaleźć przyczynę w logach.

## Kontekst
To symulacja prawdziwej pracy z monitoringiem: widzisz spike na wykresie error rate → przechodzisz do logów z tego samego okna czasowego → znajdujesz przyczynę. Ta umiejętność to rdzeń debugowania produkcyjnego.

## Zadanie
1. Uruchom symulację błędów: `curl -X POST http://localhost:8000/simulate/errors`
2. Poczekaj 2-3 minuty (niech się zbiorą dane)
3. W Explore (Prometheus) sprawdź error rate — powinien być spike
4. Zaznacz zakres czasu spike'u (kliknij i przeciągnij na wykresie)
5. Przejdź do Loki (split view lub zmień datasource) z tym samym zakresem czasu
6. Znajdź logi błędów: `{service="app"} | json | level="error"`
7. Sprawdź jakie endpointy były dotknięte
8. Zresetuj symulację: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Kliknij i przeciągnij na wykresie w Explore aby zawęzić zakres czasu. Grafana automatycznie ustawi time range na zaznaczony obszar.

</details>

<details>
<summary>Podpowiedź 2</summary>

Aby zobaczyć które endpointy miały błędy:
```logql
{service="app"} | json | level="error" | line_format "{{.endpoint}} — {{.event}}"
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Przepływ korelacji:**

1. **Metryka** (Prometheus w Explore):
```promql
sum(rate(http_requests_total{status=~"5.."}[1m]))
```
Widzisz spike error rate → zaznacz ten obszar na wykresie.

2. **Logi** (Loki — split view lub zmień datasource):
```logql
{service="app"} | json | level="error"
```
Widzisz logi z błędami w dokładnie tym samym oknie czasowym.

3. **Analiza** — jakie endpointy:
```logql
sum by (endpoint)(count_over_time({service="app"} | json | level="error" [1m]))
```
Widzisz które endpointy generowały błędy.

4. **Szczegóły** — konkretne logi:
```logql
{service="app"} | json | level="error" | line_format "{{.timestamp}} [{{.endpoint}}] {{.event}} request_id={{.request_id}}"
```

**Wniosek:** Error rate spike → logi pokazują `random_error` na wielu endpointach → przyczyna: symulacja błędów. W prawdziwym scenariuszu logi wskazałyby na np. timeout bazy danych, brakujące zasoby itp.

</details>
```

- [ ] **Step 6: Commit**

```bash
git add scenarios/03-loki-logs/
git commit -m "docs: add Chapter 3 scenarios (Loki & LogQL)"
```

---

### Task 17: Scenarios — Chapter 4 (Alerts)

**Files:**
- Create: `scenarios/04-alerts/16-first-alert.md`
- Create: `scenarios/04-alerts/17-latency-alert.md`
- Create: `scenarios/04-alerts/18-log-alert.md`
- Create: `scenarios/04-alerts/19-contact-points.md`

- [ ] **Step 1: Create 16-first-alert.md**

```markdown
# Scenariusz 16: Pierwszy alert

## Cel
Stworzyć alert w Grafanie, który powiadamia gdy error rate jest za wysoki.

## Kontekst
Alerty automatycznie informują gdy coś jest nie tak — nie musisz ciągle patrzeć na dashboard. Grafana Alerting ocenia warunki (np. "error rate > 10%") w regularnych odstępach czasu. Gdy warunek jest spełniony przez określony czas (`for`), alert zmienia stan na **Firing**.

## Zadanie
1. Otwórz Grafanę → **Alerting → Alert rules**
2. Kliknij **New alert rule**
3. Stwórz alert: "error rate > 10% przez 2 minuty"
4. Przetestuj alert — włącz symulację błędów i sprawdź czy alert zadziała

<details>
<summary>Podpowiedź 1</summary>

W sekcji "Define query and alert condition":
- Datasource: Prometheus
- Query: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
- Condition: IS ABOVE 0.1

</details>

<details>
<summary>Podpowiedź 2</summary>

"Pending period" (for) = jak długo warunek musi być spełniony zanim alert wystrzeli. Ustaw na 2 minuty. Evaluation interval = co ile sekund sprawdzać warunek (np. 30s).

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

1. **Alerting → Alert rules → New alert rule**
2. **Rule name:** High Error Rate
3. **Define query:**
   - Query A (Prometheus): `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
   - Expression B: Threshold — IS ABOVE 0.1
4. **Evaluation:**
   - Folder: nowy folder "App Alerts"
   - Evaluation group: nowa grupa "app"
   - Pending period: 2m
5. **Save rule**

**Test:**
```bash
curl -X POST http://localhost:8000/simulate/errors
# Poczekaj 3-4 minuty
# Sprawdź Alerting → Alert rules — stan powinien zmienić się na Firing
curl -X POST http://localhost:8000/simulate/reset
```

Stany alertu: **Normal** → **Pending** (warunek spełniony, czeka `for`) → **Firing** (alert aktywny).

</details>
```

- [ ] **Step 2: Create 17-latency-alert.md**

```markdown
# Scenariusz 17: Alert na latency

## Cel
Stworzyć alert gdy p95 latency przekracza 1 sekundę.

## Kontekst
Wysoki latency oznacza, że użytkownicy czekają za długo. Monitorowanie p95 (a nie średniej) łapie problemy, które dotykają "ogon" requestów — np. spowalnianie jednego endpointu.

## Zadanie
1. Stwórz nowy alert rule: "P95 latency > 1s przez 2 minuty"
2. Użyj zapytania z histogram_quantile
3. Przetestuj — włącz symulację slow i sprawdź alert

<details>
<summary>Podpowiedź 1</summary>

Query:
```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```
Condition: IS ABOVE 1

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

1. **Alerting → Alert rules → New alert rule**
2. **Rule name:** High P95 Latency
3. **Query A:** `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
4. **Expression B:** Threshold — IS ABOVE 1
5. **Folder:** App Alerts, **Group:** app
6. **Pending period:** 2m
7. **Save rule**

**Test:**
```bash
curl -X POST http://localhost:8000/simulate/slow
# Poczekaj 3-4 minuty — alert powinien przejść w Firing
curl -X POST http://localhost:8000/simulate/reset
```

</details>
```

- [ ] **Step 3: Create 18-log-alert.md**

```markdown
# Scenariusz 18: Alert na logi

## Cel
Stworzyć alert na podstawie logów — gdy pojawi się za dużo logów ERROR.

## Kontekst
Alerty na logi uzupełniają alerty na metryki. Czasem problem widać szybciej w logach (np. nowy typ błędu) niż w zagregowanych metrykach. Grafana pozwala tworzyć alerty używając Loki jako datasource.

## Zadanie
1. Stwórz alert: "więcej niż 5 logów ERROR w ciągu minuty"
2. Datasource: Loki (nie Prometheus!)
3. Przetestuj z symulacją błędów

<details>
<summary>Podpowiedź 1</summary>

Query LogQL (w trybie metrycznym):
```logql
count_over_time({service="app"} | json | level="error" [1m])
```
Condition: IS ABOVE 5

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

1. **Alerting → Alert rules → New alert rule**
2. **Rule name:** Too Many Log Errors
3. **Query A:**
   - Datasource: **Loki**
   - Query: `count_over_time({service="app"} | json | level="error" [1m])`
4. **Expression B:** Reduce → Last, then Threshold → IS ABOVE 5
5. **Folder:** App Alerts, **Group:** app
6. **Pending period:** 1m
7. **Save rule**

**Test:**
```bash
curl -X POST http://localhost:8000/simulate/errors
# Poczekaj 2 minuty — alert powinien zadziałać
curl -X POST http://localhost:8000/simulate/reset
```

</details>
```

- [ ] **Step 4: Create 19-contact-points.md**

```markdown
# Scenariusz 19: Contact points i silence

## Cel
Skonfigurować gdzie wysyłać powiadomienia i nauczyć się wyciszać alerty.

## Kontekst
**Contact point** to miejsce, gdzie trafiają powiadomienia z alertów (email, Slack, webhook). **Notification policy** decyduje który alert trafia do którego contact pointu. **Silence** pozwala tymczasowo wyciszyć alert (np. podczas planowanego maintenance).

## Zadanie
1. Stwórz contact point typu **Webhook** (nie wymaga zewnętrznych serwisów)
2. Skonfiguruj notification policy aby alerty z folderu "App Alerts" szły do tego webhooka
3. Naucz się wyciszać alert (Silence)

<details>
<summary>Podpowiedź 1</summary>

Webhook contact point: użyj `http://localhost:8000/health` jako URL (żeby zobaczyć że webhook się odpala). W prawdziwym scenariuszu byłby to Slack webhook, PagerDuty, itp.

</details>

<details>
<summary>Podpowiedź 2</summary>

Silence: Alerting → Silences → New silence. Ustaw czas trwania i matcher (np. folder="App Alerts").

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Contact point (Webhook):**
1. Alerting → Contact points → New contact point
2. Name: "Test Webhook"
3. Integration: **Webhook**
4. URL: `http://app:8000/health` (użyj nazwy Docker service, nie localhost)
5. Test → Send test notification
6. Save

**Notification policy:**
1. Alerting → Notification policies
2. New nested policy
3. Matcher: `grafana_folder = App Alerts`
4. Contact point: "Test Webhook"
5. Save

**Silence:**
1. Alerting → Silences → New silence
2. Duration: 1h
3. Label matcher: `alertname = High Error Rate`
4. Comment: "Planowany maintenance"
5. Submit

Silence wygasa automatycznie po ustawionym czasie. Możesz też ręcznie go zakończyć wcześniej (Expire).

</details>
```

- [ ] **Step 5: Commit**

```bash
git add scenarios/04-alerts/
git commit -m "docs: add Chapter 4 scenarios (Alerts)"
```

---

### Task 18: Scenarios — Chapter 5 (Break & Fix)

**Files:**
- Create: `scenarios/05-break-and-fix/20-slow-endpoint.md`
- Create: `scenarios/05-break-and-fix/21-error-storm.md`
- Create: `scenarios/05-break-and-fix/22-memory-leak.md`
- Create: `scenarios/05-break-and-fix/23-full-diagnosis.md`
- Create: `scenarios/05-break-and-fix/24-oncall-dashboard.md`

- [ ] **Step 1: Create 20-slow-endpoint.md**

```markdown
# Scenariusz 20: Wolny endpoint

## Cel
Zdiagnozować który endpoint jest wolny i udowodnić to metrykami i logami.

## Zadanie
1. Upewnij się, że generator ruchu działa (`./scripts/generate_traffic.sh`)
2. Włącz symulację: `curl -X POST http://localhost:8000/simulate/slow`
3. Poczekaj 2-3 minuty
4. **Bez zaglądania do kodu** — znajdź odpowiedzi na pytania:
   - Czy aplikacja jest wolna? Skąd wiesz?
   - Które endpointy są najwolniejsze?
   - Jaki jest p95 latency dla najwolniejszego endpointu?
   - Ile requestów jest dotkniętych?
5. Zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Zacznij od dashboardu "Application Overview" lub starter dashboardu. Panel "Request Duration (p95)" powinien pokazać wzrost.

</details>

<details>
<summary>Podpowiedź 2</summary>

Aby zobaczyć latency per endpoint:
```promql
histogram_quantile(0.95, sum by (le, endpoint)(rate(http_request_duration_seconds_bucket[5m])))
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Krok 1 — Dashboard:** Starter dashboard → "Request Duration (p95)" — widzisz wyraźny wzrost.

**Krok 2 — Który endpoint? (Prometheus Explore):**
```promql
histogram_quantile(0.95, sum by (le, endpoint)(rate(http_request_duration_seconds_bucket[5m])))
```
Wynik: `/orders` ma najwyższe p95 (1-5s), ale `/products` też jest wolniejszy niż normalnie.

**Krok 3 — Ile requestów dotkniętych:**
```promql
sum by (endpoint)(rate(http_requests_total[5m]))
```

**Krok 4 — Potwierdzenie w logach (Loki):**
```logql
{service="app"} | json | level="info" | line_format "{{.endpoint}} duration={{.duration}}"
```
Widzisz wysokie wartości `duration` w logach.

**Diagnoza:** Wszystkie endpointy są wolniejsze → problem jest globalny (nie specyficzny dla jednego endpointu). W prawdziwym scenariuszu: sprawdź bazę danych, sieć, zasoby CPU/RAM.

</details>
```

- [ ] **Step 2: Create 21-error-storm.md**

```markdown
# Scenariusz 21: Fala błędów 500

## Cel
Zdiagnozować falę błędów 500 — znaleźć przyczynę w logach i zmierzyć wpływ.

## Zadanie
1. Upewnij się, że generator ruchu działa
2. Włącz symulację: `curl -X POST http://localhost:8000/simulate/errors`
3. Poczekaj 2-3 minuty
4. **Diagnoza — odpowiedz na pytania:**
   - Jaki jest aktualny error rate?
   - Które endpointy generują błędy?
   - Co mówią logi o przyczynie?
   - Kiedy dokładnie zaczęły się błędy?
5. Zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Error rate (Prometheus):
```promql
sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) * 100
```

</details>

<details>
<summary>Podpowiedź 2</summary>

Logi błędów z timestampami (Loki):
```logql
{service="app"} | json | level="error" | line_format "{{.timestamp}} [{{.endpoint}}] {{.event}}"
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Error rate:**
```promql
sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) * 100
```
Wynik: ~30% (symulacja zwraca 500 z 30% prawdopodobieństwem).

**Które endpointy:**
```promql
sum by (endpoint)(rate(http_requests_total{status=~"5.."}[1m]))
```
Wszystkie endpointy mają błędy.

**Logi:**
```logql
{service="app"} | json | level="error"
```
Widzisz `random_error` i `order_failed` — to symulowane losowe błędy.

**Kiedy zaczęło się:**
Na wykresie error rate — znajdź moment, gdy linia poszła w górę. Zaznacz ten punkt — w logach z tego samego czasu pojawią się pierwsze wpisy error.

**Timeline:** error rate 0% → spike do ~30% → trwa stabilnie → reset → powrót do 0%.

</details>
```

- [ ] **Step 3: Create 22-memory-leak.md**

```markdown
# Scenariusz 22: Wyciek pamięci

## Cel
Zaobserwować wyciek pamięci w metrykach i zidentyfikować trend.

## Zadanie
1. Upewnij się, że generator ruchu działa
2. Włącz symulację: `curl -X POST http://localhost:8000/simulate/memory-leak`
3. Obserwuj przez 5 minut
4. **Diagnoza:**
   - Jak zmienia się zużycie pamięci aplikacji?
   - Jaki jest trend — liniowy, wykładniczy?
   - Ile pamięci przybywa na minutę?
   - Po jakim czasie aplikacja mogłaby się "wywrócić"?
5. Zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Metryka pamięci procesu:
```promql
process_resident_memory_bytes{job="fastapi-app"}
```

Albo custom metryka wycieku:
```promql
memory_leak_bytes
```

</details>

<details>
<summary>Podpowiedź 2</summary>

Aby zobaczyć przyrost na minutę:
```promql
rate(memory_leak_bytes[1m])
```

Żeby przeliczyć na MB — podziel przez 1024*1024.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Zużycie pamięci (surowe):**
```promql
process_resident_memory_bytes{job="fastapi-app"} / 1024 / 1024
```
Widzisz rosnący wykres (w MB).

**Custom metryka wycieku:**
```promql
memory_leak_bytes / 1024 / 1024
```
Rośnie liniowo — ~100KB na request.

**Przyrost per minutę:**
```promql
rate(memory_leak_bytes[1m]) / 1024 / 1024
```

**Trend:** Liniowy — każdy request dodaje ~100KB. Im większy ruch, tym szybciej rośnie pamięć.

**Status wycieku:**
```bash
curl http://localhost:8000/simulate/status
```
Pokaże `leak_size_mb`.

W prawdziwym scenariuszu wyciek pamięci prowadzi do OOM Kill — kontener zostaje zabity przez system.

</details>
```

- [ ] **Step 4: Create 23-full-diagnosis.md**

```markdown
# Scenariusz 23: Pełna diagnoza

## Cel
Zdiagnozować sytuację gdy wszystko się psuje jednocześnie — zbudować timeline incydentu.

## Zadanie
1. Upewnij się, że generator ruchu działa
2. Włącz WSZYSTKIE symulacje naraz:
   ```bash
   curl -X POST http://localhost:8000/simulate/slow
   curl -X POST http://localhost:8000/simulate/errors
   curl -X POST http://localhost:8000/simulate/memory-leak
   ```
3. Poczekaj 3-5 minut
4. **Zbuduj timeline incydentu — odpowiedz:**
   - Jakie problemy widzisz? Wymień wszystkie
   - W jakiej kolejności byś je priorytetyzował?
   - Które metryki/logi pomogły Ci je znaleźć?
   - Jaki dashboard/widok najlepiej pokazuje pełny obraz?
5. Zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Zacznij od przeglądu dashboardu — co od razu rzuca się w oczy? Potem Explore → Prometheus, potem Loki.

</details>

<details>
<summary>Podpowiedź 2</summary>

Priorytetyzacja: błędy (użytkownicy nie mogą korzystać) > latency (mogą, ale wolno) > memory leak (jeszcze działa, ale się pogorszy).

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Timeline incydentu:**

| Czas | Problem | Źródło | Metryka/Log |
|------|---------|--------|-------------|
| T+0 | Włączenie symulacji | — | — |
| T+1m | Error rate rośnie do ~30% | Dashboard → Error Rate panel | `rate(http_requests_total{status=~"5.."}[1m])` |
| T+1m | P95 latency rośnie > 1s | Dashboard → Latency panel | `histogram_quantile(0.95, ...)` |
| T+1m | Pamięć zaczyna rosnąć | Prometheus Explore | `process_resident_memory_bytes` |
| T+2m | Alerty zaczynają strzelać | Alerting page | Alert rules w stanie Firing |
| T+3m | Logi pełne errorów | Loki Explore | `{service="app"} \| json \| level="error"` |

**Priorytetyzacja:**
1. 🔴 **Błędy 500** — użytkownicy nie mogą składać zamówień
2. 🟡 **Wysoki latency** — użytkownicy czekają zbyt długo
3. 🟠 **Memory leak** — nie wpływa natychmiast, ale pogorszy się z czasem

**Najlepszy widok:** Split view w Explore (Prometheus + Loki) z tym samym zakresem czasu, plus otwarty dashboard "Application Overview" w osobnej zakładce.

</details>
```

- [ ] **Step 5: Create 24-oncall-dashboard.md**

```markdown
# Scenariusz 24: Dashboard On-Call

## Cel
Zbudować dashboard, który pokazuje zdrowie systemu "na jeden rzut oka" — przydatny podczas dyżuru (on-call).

## Zadanie
Stwórz nowy dashboard **"On-Call"** zawierający wszystko, czego potrzebujesz żeby ocenić stan systemu w 10 sekund. Wykorzystaj wiedzę ze wszystkich poprzednich scenariuszy.

**Wymagania:**
1. **Górny rząd** — kluczowe liczby (Stat panele):
   - Aktualny error rate (%)
   - P95 latency (sekundy)
   - RPS (requests per second)
   - Uptime aplikacji
2. **Środkowy rząd** — wykresy w czasie (Time series):
   - Error rate w czasie
   - Latency p50/p95/p99 na jednym wykresie
   - RPS per endpoint
3. **Dolny rząd** — kontekst:
   - Ostatnie logi ERROR (panel Logs z Loki)
   - Zużycie pamięci aplikacji (Time series)
4. **Zmienne** — dropdown do filtrowania po endpoincie
5. **Auto-refresh** — co 10 sekund

<details>
<summary>Podpowiedź 1</summary>

Zapytania do użycia (znasz je z wcześniejszych scenariuszy):

- Error rate: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100`
- P95 latency: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
- RPS: `sum(rate(http_requests_total[1m]))`
- Uptime: `process_uptime_seconds{job="fastapi-app"}`
- Memory: `process_resident_memory_bytes{job="fastapi-app"} / 1024 / 1024`
- Logs: `{service="app"} | json | level="error"`

</details>

<details>
<summary>Podpowiedź 2</summary>

Trzy percentyle na jednym wykresie — dodaj 3 query w jednym panelu:
- Query A: `histogram_quantile(0.5, ...)` → Legend: p50
- Query B: `histogram_quantile(0.95, ...)` → Legend: p95
- Query C: `histogram_quantile(0.99, ...)` → Legend: p99

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

To jest Twój dashboard — nie ma jednego "poprawnego" rozwiązania. Oto propozycja:

**Górny rząd (h=4, 4 panele Stat po w=6):**

| Panel | Query | Unit | Thresholds |
|-------|-------|------|-----------|
| Error Rate | `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100` | percent | green<5, yellow<10, red≥10 |
| P95 Latency | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` | seconds | green<0.5, yellow<1, red≥1 |
| RPS | `sum(rate(http_requests_total{endpoint=~"$endpoint"}[1m]))` | reqps | — |
| Uptime | `process_uptime_seconds{job="fastapi-app"}` | duration(s) | — |

**Środkowy rząd (h=8, 3 panele Time series):**

| Panel | Queries |
|-------|---------|
| Error Rate Over Time | `sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) * 100` |
| Latency Percentiles | p50 + p95 + p99 (3 queries) |
| RPS per Endpoint | `sum(rate(http_requests_total{endpoint=~"$endpoint"}[1m])) by (endpoint)` |

**Dolny rząd (h=8, 2 panele):**

| Panel | Typ | Query |
|-------|-----|-------|
| Recent Errors | Logs (Loki) | `{service="app"} \| json \| level="error"` |
| Memory Usage (MB) | Time series | `process_resident_memory_bytes{job="fastapi-app"} / 1024 / 1024` |

**Zmienne:** `endpoint` → `label_values(http_requests_total, endpoint)` (Multi-value + All)

**Auto-refresh:** Dashboard settings → prawym górnym rogu → ikona refresh → 10s

**Test:** Uruchom symulacje i obserwuj jak dashboard reaguje na problemy.

Gratulacje — ukończyłeś wszystkie 24 scenariusze! 🎉

</details>
```

- [ ] **Step 6: Commit**

```bash
git add scenarios/05-break-and-fix/
git commit -m "docs: add Chapter 5 scenarios (Break & Fix)"
```

---

### Task 19: Final verification

- [ ] **Step 1: Verify all files exist**

```bash
cd /home/kkopec/projects/grafana-prometheus-lab
find . -type f | sort
```

Expected: all files from the file structure section present.

- [ ] **Step 2: Full stack test**

```bash
docker compose up -d --build
sleep 15
docker compose ps
curl -s http://localhost:8000/health
curl -s http://localhost:8000/products
curl -s http://localhost:8000/metrics | head -5
curl -s http://localhost:9090/api/v1/targets | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']['activeTargets']), 'targets')"
curl -s http://localhost:3000/api/health
curl -s http://localhost:3000/api/datasources | python3 -c "import sys,json; d=json.load(sys.stdin); print([ds['name'] for ds in d])"
docker compose down
```

Expected: 6 services running, FastAPI responds, 3 Prometheus targets, Grafana healthy with 2 datasources.

- [ ] **Step 3: Final commit if any changes remain**

```bash
git status
# If any unstaged changes:
git add -A
git commit -m "chore: final cleanup"
```
