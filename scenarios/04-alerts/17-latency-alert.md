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
