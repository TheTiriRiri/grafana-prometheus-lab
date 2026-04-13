# Scenariusz 10: Adnotacje

## Cel
Dodać adnotacje do dashboardu — wizualne znaczniki na osi czasu pokazujące ważne wydarzenia.

## Kontekst
Adnotacje (annotations) to pionowe linie na wykresach, które oznaczają momenty zdarzeń — np. deploy, restart, zmiana konfiguracji. Pomagają korelować zmiany w metrykach z wydarzeniami. Można je dodawać ręcznie lub automatycznie na podstawie zapytań.

## Zadanie
1. Otwórz dashboard "Application Overview"
2. Dodaj ręczną adnotację: kliknij na wykresie w dowolnym miejscu, wybierz "Add annotation", wpisz "Test deploy"
3. Stwórz automatyczną adnotację na podstawie zmian metryki:
   - Dashboard Settings → Annotations → New annotation query
   - Pokaż momenty gdy error rate przekroczył 5%

<details>
<summary>Podpowiedź 1</summary>

Ręczna adnotacja: kliknij i przytrzymaj na wykresie → pojawi się menu z opcją "Add annotation".

</details>

<details>
<summary>Podpowiedź 2</summary>

Automatyczna adnotacja — to jest bardziej zaawansowane. Użyj datasource Prometheus i zapytania:
```promql
sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) > 0.05
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Ręczna adnotacja:**
1. Na dowolnym panelu typu Time series — kliknij i przytrzymaj na wykresie
2. Pojawi się opcja "Add annotation"
3. Wpisz tekst: "Test deploy" → Save

**Automatyczna adnotacja:**
1. Dashboard Settings (⚙️) → Annotations → New annotation query
2. Name: "High Error Rate"
3. Data source: Prometheus
4. Query: `sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) > 0.05`
5. Color: red
6. Apply → Save dashboard

Aby zobaczyć automatyczną adnotację, uruchom symulację błędów:
```bash
curl -X POST http://localhost:8000/simulate/errors
```
Poczekaj 2-3 minuty, potem zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

</details>
