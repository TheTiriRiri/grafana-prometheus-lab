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
