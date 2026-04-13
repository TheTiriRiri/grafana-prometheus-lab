# Scenariusz 9: Gauge i Stat panele

## Cel
Stworzyć panele pokazujące pojedyncze wartości — aktualny stan magazynu i uptime aplikacji.

## Kontekst
Nie wszystkie dane najlepiej pokazywać jako wykres w czasie. **Stat** pokazuje jedną dużą liczbę (np. error rate). **Gauge** to "zegar" z kolorową skalą (np. stan magazynu). Oba świetnie nadają się do wartości, które chcesz zobaczyć "na pierwszy rzut oka".

## Zadanie
1. Do dashboardu "Application Overview" dodaj panel **Stat** z uptime aplikacji
   - Metryka: `time() - process_start_time_seconds{job="fastapi-app"}`
   - Unit: seconds (duration)
2. Dodaj panel **Gauge** z liczbą produktów w magazynie
   - Metryka: `products_in_stock`
   - Thresholds: czerwony < 50, żółty 50-100, zielony > 100

<details>
<summary>Podpowiedź 1</summary>

`process_start_time_seconds` to wbudowana metryka z `prometheus_client`. `time()` to aktualny czas w PromQL. Różnica daje uptime.

</details>

<details>
<summary>Podpowiedź 2</summary>

Dla panelu Stat z uptime: wybierz Unit → Time → seconds (s). Grafana automatycznie sformatuje na "2h 34m 12s".

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Panel Uptime (Stat):**
- Typ: Stat
- Query: `time() - process_start_time_seconds{job="fastapi-app"}`
- Unit: duration (seconds)
- Tytuł: "App Uptime"

**Panel Products in Stock (Gauge):**
- Typ: Gauge
- Query: `products_in_stock`
- Min: 0, Max: 300
- Thresholds: red=null (default), yellow=50, green=100
- Tytuł: "Products in Stock"

Zapisz dashboard.

</details>
