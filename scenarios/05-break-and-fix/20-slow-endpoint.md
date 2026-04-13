# Scenariusz 20: Wolny endpoint

## Cel
Zdiagnozować który endpoint jest wolny i udowodnić to metrykami i logami.

## Zadanie
1. Upewnij się, że generator ruchu działa (`./scripts/generate_traffic.sh`)
2. Włącz symulację: `curl -X POST http://localhost:8000/simulate/slow`
3. Poczekaj 2-3 minuty
4. **Bez zaglądania do kodu** — znajdź odpowiedzi na pytania:
   - Czy aplikacja jest wolna? Skąd wiesz?
   - Które endpointy są najwolniejsze?
   - Jaki jest p95 latency dla najwolniejszego endpointu?
   - Ile requestów jest dotkniętych?
5. Zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Zacznij od dashboardu "Application Overview" lub starter dashboardu. Panel "Request Duration (p95)" powinien pokazać wzrost.

</details>

<details>
<summary>Podpowiedź 2</summary>

Aby zobaczyć latency per endpoint:
```promql
histogram_quantile(0.95, sum by (le, endpoint)(rate(http_request_duration_seconds_bucket[5m])))
```

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Krok 1 — Dashboard:** Starter dashboard → "Request Duration (p95)" — widzisz wyraźny wzrost.

**Krok 2 — Który endpoint? (Prometheus Explore):**
```promql
histogram_quantile(0.95, sum by (le, endpoint)(rate(http_request_duration_seconds_bucket[5m])))
```
Wynik: `/orders` ma najwyższe p95 (1-5s), ale `/products` też jest wolniejszy niż normalnie.

**Krok 3 — Ile requestów dotkniętych:**
```promql
sum by (endpoint)(rate(http_requests_total[5m]))
```

**Krok 4 — Potwierdzenie w logach (Loki):**
```logql
{service="app"} | json | level="info" | line_format "{{.endpoint}} duration={{.duration}}"
```
Widzisz wysokie wartości `duration` w logach.

**Diagnoza:** Wszystkie endpointy są wolniejsze → problem jest globalny (nie specyficzny dla jednego endpointu). W prawdziwym scenariuszu: sprawdź bazę danych, sieć, zasoby CPU/RAM.

</details>
