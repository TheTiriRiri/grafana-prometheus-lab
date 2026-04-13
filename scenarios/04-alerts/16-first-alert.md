# Scenariusz 16: Pierwszy alert

## Cel
Stworzyć alert w Grafanie, który powiadamia gdy error rate jest za wysoki.

## Kontekst
Alerty automatycznie informują gdy coś jest nie tak — nie musisz ciągle patrzeć na dashboard. Grafana Alerting ocenia warunki (np. "error rate > 10%") w regularnych odstępach czasu. Gdy warunek jest spełniony przez określony czas (`for`), alert zmienia stan na **Firing**.

## Zadanie
1. Otwórz Grafanę → **Alerting → Alert rules**
2. Kliknij **New alert rule**
3. Stwórz alert: "error rate > 10% przez 2 minuty"
4. Przetestuj alert — włącz symulację błędów i sprawdź czy alert zadziała

<details>
<summary>Podpowiedź 1</summary>

W sekcji "Define query and alert condition":
- Datasource: Prometheus
- Query: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
- Condition: IS ABOVE 0.1

</details>

<details>
<summary>Podpowiedź 2</summary>

"Pending period" (for) = jak długo warunek musi być spełniony zanim alert wystrzeli. Ustaw na 2 minuty. Evaluation interval = co ile sekund sprawdzać warunek (np. 30s).

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

1. **Alerting → Alert rules → New alert rule**
2. **Rule name:** High Error Rate
3. **Define query:**
   - Query A (Prometheus): `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
   - Expression B: Threshold — IS ABOVE 0.1
4. **Evaluation:**
   - Folder: nowy folder "App Alerts"
   - Evaluation group: nowa grupa "app"
   - Pending period: 2m
5. **Save rule**

**Test:**
```bash
curl -X POST http://localhost:8000/simulate/errors
# Poczekaj 3-4 minuty
# Sprawdź Alerting → Alert rules — stan powinien zmienić się na Firing
curl -X POST http://localhost:8000/simulate/reset
```

Stany alertu: **Normal** → **Pending** (warunek spełniony, czeka `for`) → **Firing** (alert aktywny).

</details>
