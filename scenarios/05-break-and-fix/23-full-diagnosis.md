# Scenariusz 23: Pełna diagnoza

## Cel
Zdiagnozować sytuację gdy wszystko się psuje jednocześnie — zbudować timeline incydentu.

## Zadanie
1. Upewnij się, że generator ruchu działa
2. Włącz WSZYSTKIE symulacje naraz:
   ```bash
   curl -X POST http://localhost:8000/simulate/slow
   curl -X POST http://localhost:8000/simulate/errors
   curl -X POST http://localhost:8000/simulate/memory-leak
   ```
3. Poczekaj 3-5 minut
4. **Zbuduj timeline incydentu — odpowiedz:**
   - Jakie problemy widzisz? Wymień wszystkie
   - W jakiej kolejności byś je priorytetyzował?
   - Które metryki/logi pomogły Ci je znaleźć?
   - Jaki dashboard/widok najlepiej pokazuje pełny obraz?
5. Zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Zacznij od przeglądu dashboardu — co od razu rzuca się w oczy? Potem Explore → Prometheus, potem Loki.

</details>

<details>
<summary>Podpowiedź 2</summary>

Priorytetyzacja: błędy (użytkownicy nie mogą korzystać) > latency (mogą, ale wolno) > memory leak (jeszcze działa, ale się pogorszy).

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Timeline incydentu:**

| Czas | Problem | Źródło | Metryka/Log |
|------|---------|--------|-------------|
| T+0 | Włączenie symulacji | — | — |
| T+1m | Error rate rośnie do ~30% | Dashboard → Error Rate panel | `rate(http_requests_total{status=~"5.."}[1m])` |
| T+1m | P95 latency rośnie > 1s | Dashboard → Latency panel | `histogram_quantile(0.95, ...)` |
| T+1m | Pamięć zaczyna rosnąć | Prometheus Explore | `process_resident_memory_bytes` |
| T+2m | Alerty zaczynają strzelać | Alerting page | Alert rules w stanie Firing |
| T+3m | Logi pełne errorów | Loki Explore | `{service="app"} \| json \| level="error"` |

**Priorytetyzacja:**
1. 🔴 **Błędy 500** — użytkownicy nie mogą składać zamówień
2. 🟡 **Wysoki latency** — użytkownicy czekają zbyt długo
3. 🟠 **Memory leak** — nie wpływa natychmiast, ale pogorszy się z czasem

**Najlepszy widok:** Split view w Explore (Prometheus + Loki) z tym samym zakresem czasu, plus otwarty dashboard "Application Overview" w osobnej zakładce.

</details>
