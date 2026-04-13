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
