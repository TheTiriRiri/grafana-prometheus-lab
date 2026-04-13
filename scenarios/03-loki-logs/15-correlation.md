# Scenariusz 15: Korelacja logi i metryki

## Cel
Po zaobserwowaniu anomalii w metrykach, znaleźć przyczynę w logach.

## Kontekst
To symulacja prawdziwej pracy z monitoringiem: widzisz spike na wykresie error rate → przechodzisz do logów z tego samego okna czasowego → znajdujesz przyczynę. Ta umiejętność to rdzeń debugowania produkcyjnego.

## Zadanie
1. Uruchom symulację błędów: `curl -X POST http://localhost:8000/simulate/errors`
2. Poczekaj 2-3 minuty (niech się zbiorą dane)
3. W Explore (Prometheus) sprawdź error rate — powinien być spike
4. Zaznacz zakres czasu spike'u (kliknij i przeciągnij na wykresie)
5. Przejdź do Loki (split view lub zmień datasource) z tym samym zakresem czasu
6. Znajdź logi błędów: `{service="app"} | json | level="error"`
7. Sprawdź jakie endpointy były dotknięte
8. Zresetuj symulację: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Kliknij i przeciągnij na wykresie w Explore aby zawęzić zakres czasu. Grafana automatycznie ustawi time range na zaznaczony obszar.

</details>

<details>
<summary>Podpowiedź 2</summary>

Aby zobaczyć które endpointy miały błędy:
```logql
{service="app"} | json | level="error" | line_format "{{.endpoint}} — {{.event}}"
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Przepływ korelacji:**

1. **Metryka** (Prometheus w Explore):
```promql
sum(rate(http_requests_total{status=~"5.."}[1m]))
```
Widzisz spike error rate → zaznacz ten obszar na wykresie.

2. **Logi** (Loki — split view lub zmień datasource):
```logql
{service="app"} | json | level="error"
```
Widzisz logi z błędami w dokładnie tym samym oknie czasowym.

3. **Analiza** — jakie endpointy:
```logql
sum by (endpoint)(count_over_time({service="app"} | json | level="error" [1m]))
```
Widzisz które endpointy generowały błędy.

4. **Szczegóły** — konkretne logi:
```logql
{service="app"} | json | level="error" | line_format "{{.timestamp}} [{{.endpoint}}] {{.event}} request_id={{.request_id}}"
```

**Wniosek:** Error rate spike → logi pokazują `random_error` na wielu endpointach → przyczyna: symulacja błędów. W prawdziwym scenariuszu logi wskazałyby na np. timeout bazy danych, brakujące zasoby itp.

</details>
