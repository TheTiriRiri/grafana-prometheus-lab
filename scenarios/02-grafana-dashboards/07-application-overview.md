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
