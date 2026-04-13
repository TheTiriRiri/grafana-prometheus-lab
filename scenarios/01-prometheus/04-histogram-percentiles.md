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
