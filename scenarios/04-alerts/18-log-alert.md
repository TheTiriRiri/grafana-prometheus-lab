# Scenariusz 18: Alert na logi

## Cel
Stworzyć alert na podstawie logów — gdy pojawi się za dużo logów ERROR.

## Kontekst
Alerty na logi uzupełniają alerty na metryki. Czasem problem widać szybciej w logach (np. nowy typ błędu) niż w zagregowanych metrykach. Grafana pozwala tworzyć alerty używając Loki jako datasource.

## Zadanie
1. Stwórz alert: "więcej niż 5 logów ERROR w ciągu minuty"
2. Datasource: Loki (nie Prometheus!)
3. Przetestuj z symulacją błędów

<details>
<summary>Podpowiedź 1</summary>

Query LogQL (w trybie metrycznym):
```logql
count_over_time({service="app"} | json | level="error" [1m])
```
Condition: IS ABOVE 5

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

1. **Alerting → Alert rules → New alert rule**
2. **Rule name:** Too Many Log Errors
3. **Query A:**
   - Datasource: **Loki**
   - Query: `count_over_time({service="app"} | json | level="error" [1m])`
4. **Expression B:** Reduce → Last, then Threshold → IS ABOVE 5
5. **Folder:** App Alerts, **Group:** app
6. **Pending period:** 1m
7. **Save rule**

**Test:**
```bash
curl -X POST http://localhost:8000/simulate/errors
# Poczekaj 2 minuty — alert powinien zadziałać
curl -X POST http://localhost:8000/simulate/reset
```

</details>
