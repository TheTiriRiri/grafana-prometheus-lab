# Scenariusz 11: Explore w Grafanie

## Cel
Znaleźć logi aplikacji w Grafana Explore i nauczyć się podstawowej nawigacji.

## Kontekst
**Loki** to system agregacji logów — odpowiednik Prometheusa, ale dla logów. Loki nie indeksuje treści logów (jak Elasticsearch), tylko ich **labele**. To sprawia, że jest lekki i szybki. Logi przeglądamy przez **Grafana Explore** — tryb ad-hoc do eksplorowania danych.

## Zadanie
1. Otwórz Grafanę: http://localhost:3000
2. Kliknij ikonę kompasu w lewym menu → **Explore**
3. W górnym dropdownie wybierz datasource: **Loki**
4. W polu zapytania wpisz: `{service="app"}`
5. Kliknij **Run query**
6. Spróbuj też: `{service="prometheus"}` i `{service="grafana"}`
7. Odpowiedz: jakie labele mają Twoje logi?

<details>
<summary>Podpowiedź 1</summary>

Label `service` pochodzi z konfiguracji Promtail — mapuje docker-compose service name na label loga.

</details>

<details>
<summary>Podpowiedź 2</summary>

Rozwiń pojedynczy wpis loga klikając na niego. Zobaczysz surową treść (JSON) i wykryte labele.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

Zapytanie `{service="app"}` pokazuje logi z kontenera aplikacji FastAPI. Każdy log to JSON:

```json
{"request_id": "a1b2c3d4", "endpoint": "/products", "event": "products_listed", "level": "info", "timestamp": "2026-04-14T10:23:45.123Z"}
```

**Dostępne labele** (widoczne po rozwinięciu loga):
- `service` — nazwa serwisu z docker-compose (app, prometheus, grafana...)
- `container` — nazwa kontenera Docker
- `logstream` — stdout lub stderr

Logi z `{service="app"}` to strukturalne logi JSON z naszej aplikacji FastAPI (skonfigurowane przez `structlog`).

</details>
