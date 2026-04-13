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
- Uptime: `time() - process_start_time_seconds{job="fastapi-app"}`
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
| Uptime | `time() - process_start_time_seconds{job="fastapi-app"}` | duration(s) | — |

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
