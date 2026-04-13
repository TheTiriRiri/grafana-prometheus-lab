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
