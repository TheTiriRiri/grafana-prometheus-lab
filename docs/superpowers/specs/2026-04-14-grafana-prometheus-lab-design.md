# Grafana + Prometheus + Loki Learning Lab — Design Spec

## Overview

Projekt edukacyjny do nauki monitoringu (Grafana, Prometheus, Loki) w Dockerze.
Skierowany do początkującego backend developera (Python/FastAPI).

**Podejście:** Gotowa infrastruktura (jeden `docker-compose up`) + 24 scenariusze/zadania pogrupowane w 5 rozdziałów o rosnącej trudności. Późniejsze rozdziały zawierają scenariusze "break & fix" symulujące realne awarie.

---

## Architektura stacku

```
┌─────────────────────────────────────────────────────┐
│                    Docker Network                    │
│                                                      │
│  ┌──────────┐    scrape     ┌────────────┐          │
│  │Prometheus │◄─────────────│ FastAPI App │          │
│  │  :9090    │              │   :8000     │          │
│  └─────┬─────┘              └──────┬──────┘          │
│        │                          │ stdout logs      │
│        │                          ▼                  │
│        │                   ┌────────────┐            │
│        │                   │  Promtail  │            │
│        │                   └──────┬─────┘            │
│        │                          │ push             │
│        │                          ▼                  │
│        │                   ┌────────────┐            │
│        │                   │    Loki    │            │
│        │                   │   :3100    │            │
│        │                   └──────┬─────┘            │
│        │                          │                  │
│        ▼                          ▼                  │
│  ┌────────────────────────────────────────┐          │
│  │              Grafana :3000              │          │
│  │  (datasources: Prometheus + Loki)      │          │
│  └────────────────────────────────────────┘          │
│                                                      │
│  ┌──────────────┐                                    │
│  │node-exporter │ (metryki hosta: CPU, RAM, dysk)   │
│  │   :9100      │                                    │
│  └──────────────┘                                    │
└─────────────────────────────────────────────────────┘
```

### Komponenty

- **FastAPI App (:8000)** — przykładowa aplikacja sklepu internetowego, eksponuje metryki Prometheus (`/metrics`), loguje strukturalnie (JSON)
- **Prometheus (:9090)** — zbiera metryki z FastAPI i node-exporter co 15s
- **Loki (:3100)** — agregacja logów
- **Promtail** — zbiera logi z kontenerów Docker i wysyła do Loki
- **Grafana (:3000)** — wizualizacja, dashboardy, alerty. Auto-provisioned datasources + starter dashboard
- **node-exporter (:9100)** — metryki systemowe hosta (CPU, RAM, dysk)

Wszystko uruchamiane jednym `docker-compose up -d`.

---

## Aplikacja FastAPI

### Endpointy

| Endpoint | Metoda | Opis | Rola w nauce |
|---|---|---|---|
| `/products` | GET | Lista produktów | Bazowy ruch, metryki request count |
| `/products/{id}` | GET | Szczegóły produktu | 404 gdy nie istnieje — error rate |
| `/orders` | POST | Złóż zamówienie | Wolniejszy endpoint — latency |
| `/health` | GET | Healthcheck | Monitoring dostępności |
| `/metrics` | GET | Metryki Prometheus | Scraped przez Prometheus |
| `/simulate/slow` | POST | Włącz losowe opóźnienia | Break & fix |
| `/simulate/errors` | POST | Włącz losowe błędy 500 | Break & fix |
| `/simulate/memory-leak` | POST | Symuluj rosnące zużycie pamięci | Break & fix |
| `/simulate/reset` | POST | Reset wszystkich symulacji | Break & fix |

### Metryki Prometheus

Automatyczne (via `prometheus-fastapi-instrumentator`):
- `http_requests_total` — counter, labele: method, endpoint, status
- `http_request_duration_seconds` — histogram

Custom:
- `orders_total` — counter, złożone zamówienia
- `orders_processing_seconds` — histogram, czas przetwarzania zamówienia
- `products_in_stock` — gauge, ile produktów w magazynie

### Logi

Strukturalne JSON logi (via `structlog`):
- timestamp, level, message, request_id, endpoint, status_code

---

## Scenariusze — 5 rozdziałów, 24 zadania

Każdy scenariusz to osobny plik Markdown z sekcjami:
- **Cel** — co się nauczysz
- **Kontekst** — niezbędna wiedza
- **Zadanie** — co musisz zrobić
- **Podpowiedzi** — ukryte hinty (do odkrycia gdy utkniesz)
- **Rozwiązanie** — pełne rozwiązanie z wyjaśnieniem

### Rozdział 1: Prometheus — metryki i PromQL (scenariusze 1-5)

1. **Poznaj targety** — otwórz Prometheus UI, sprawdź jakie targety są scrapowane, zrozum status "UP"
2. **Pierwsze zapytanie PromQL** — znajdź ile requestów obsłużyła aplikacja, użyj `http_requests_total`
3. **Rate i Counter** — oblicz RPS (requests per second) za ostatnie 5 minut używając `rate()`
4. **Histogram i percentyle** — znajdź p50, p95 i p99 latency endpointu `/orders`
5. **Filtrowanie labelami** — znajdź error rate (procent odpowiedzi 5xx) per endpoint

### Rozdział 2: Grafana — dashboardy (scenariusze 6-10)

6. **Pierwszy panel** — stwórz panel z wykresem RPS w czasie
7. **Dashboard "Application Overview"** — zbuduj dashboard z 4 panelami: RPS, latency p95, error rate, status kodów (pie chart)
8. **Zmienne (variables)** — dodaj dropdown do filtrowania dashboardu po endpoincie
9. **Gauge i Stat panele** — stwórz panel pokazujący aktualną liczbę produktów w magazynie i uptime aplikacji
10. **Adnotacje** — dodaj adnotacje pokazujące momenty deployów/restartów

### Rozdział 3: Loki — logi i LogQL (scenariusze 11-15)

11. **Explore w Grafanie** — znajdź logi aplikacji w Grafana Explore, filtruj po kontenerze
12. **LogQL — filtrowanie** — znajdź wszystkie logi z błędami (level=error), policz ile ich było
13. **LogQL — parsowanie** — wyciągnij `request_id` i `status_code` z JSON logów, stwórz metrykę z logów
14. **Dashboard z logami** — dodaj panel z logami do istniejącego dashboardu, połącz z metrykami (split view)
15. **Korelacja logi <-> metryki** — po spike'u w error rate, znajdź konkretne logi z błędami w tym samym oknie czasowym

### Rozdział 4: Alerty (scenariusze 16-19)

16. **Pierwszy alert w Grafanie** — stwórz alert: "error rate > 10% przez 2 minuty"
17. **Alert na latency** — alert gdy p95 latency > 1s
18. **Alert na logi** — alert gdy pojawi się więcej niż 5 logów ERROR w ciągu minuty
19. **Contact points i silence** — skonfiguruj wysyłanie alertów (webhook/email), naucz się wyciszać alerty

### Rozdział 5: Break & Fix — diagnozowanie problemów (scenariusze 20-24)

20. **Wolny endpoint** — włącz symulację slow, zdiagnozuj który endpoint jest wolny, udowodnij to metrykami
21. **Fala błędów 500** — włącz symulację errors, znajdź przyczynę w logach, zmierz wpływ na error rate
22. **Wyciek pamięci** — włącz symulację memory leak, zaobserwuj trend w metrykach, zidentyfikuj problem
23. **Pełna diagnoza** — wszystkie symulacje włączone jednocześnie, zbuduj timeline: co się zepsuło, kiedy, jaka przyczyna
24. **Stwórz własny dashboard "On-Call"** — na podstawie doświadczeń z poprzednich scenariuszy, zbuduj dashboard który pokazuje zdrowie systemu "na jeden rzut oka"

---

## Struktura plików

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
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── datasources.yml
│   │   └── dashboards/
│   │       ├── dashboards.yml
│   │       └── starter.json
│   └── grafana.ini
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

## Git i środowisko lokalne

- **Git** — projekt inicjalizowany jako repozytorium git od pierwszego kroku
- **`.gitignore`** — wyklucza: `.venv/`, `__pycache__/`, `*.pyc`, `.env`, dane wolumenów Docker (Prometheus, Loki, Grafana storage)
- **`.venv`** — lokalne wirtualne środowisko Python do wsparcia IDE (autocompletion, linting). Aplikacja działa w Dockerze, ale `.venv` z zainstalowanymi zależnościami (`pip install -r app/requirements.txt`) daje komfort pracy w edytorze. README opisuje jak je stworzyć.

---

## Kluczowe decyzje

- **Grafana bez logowania** — anonymous admin, zero barier w nauce
- **Auto-provisioning** — datasources i starter dashboard gotowe po `docker-compose up`
- **Jeden `docker-compose.yml`** — cały stack jednym poleceniem
- **Skrypt generowania ruchu** — `generate_traffic.sh` (curl w pętli) zapewnia dane w metrykach i logach
- **Symulacje awarii via API** — endpointy `/simulate/*` pozwalają włączać/wyłączać problemy bez restartowania kontenerów
- **Scenariusze po polsku** — cała dokumentacja i zadania w języku polskim
- **JSON logi** — ułatwiają parsowanie w LogQL, bardziej realistyczne niż plain text
