# Scenariusz 22: Wyciek pamięci

## Cel
Zaobserwować wyciek pamięci w metrykach i zidentyfikować trend.

## Zadanie
1. Upewnij się, że generator ruchu działa
2. Włącz symulację: `curl -X POST http://localhost:8000/simulate/memory-leak`
3. Obserwuj przez 5 minut
4. **Diagnoza:**
   - Jak zmienia się zużycie pamięci aplikacji?
   - Jaki jest trend — liniowy, wykładniczy?
   - Ile pamięci przybywa na minutę?
   - Po jakim czasie aplikacja mogłaby się "wywrócić"?
5. Zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

<details>
<summary>Podpowiedź 1</summary>

Metryka pamięci procesu:
```promql
process_resident_memory_bytes{job="fastapi-app"}
```

Albo custom metryka wycieku:
```promql
memory_leak_bytes
```

</details>

<details>
<summary>Podpowiedź 2</summary>

Aby zobaczyć przyrost na minutę:
```promql
rate(memory_leak_bytes[1m])
```

Żeby przeliczyć na MB — podziel przez 1024*1024.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Zużycie pamięci (surowe):**
```promql
process_resident_memory_bytes{job="fastapi-app"} / 1024 / 1024
```
Widzisz rosnący wykres (w MB).

**Custom metryka wycieku:**
```promql
memory_leak_bytes / 1024 / 1024
```
Rośnie liniowo — ~100KB na request.

**Przyrost per minutę:**
```promql
rate(memory_leak_bytes[1m]) / 1024 / 1024
```

**Trend:** Liniowy — każdy request dodaje ~100KB. Im większy ruch, tym szybciej rośnie pamięć.

**Status wycieku:**
```bash
curl http://localhost:8000/simulate/status
```
Pokaże `leak_size_mb`.

W prawdziwym scenariuszu wyciek pamięci prowadzi do OOM Kill — kontener zostaje zabity przez system.

</details>
