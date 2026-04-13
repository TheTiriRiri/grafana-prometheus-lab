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
