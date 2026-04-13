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
