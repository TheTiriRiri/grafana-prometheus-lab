# Scenariusz 12: LogQL — filtrowanie

## Cel
Nauczyć się filtrować logi po treści i liczyć je.

## Kontekst
**LogQL** to język zapytań Loki (odpowiednik PromQL dla logów). Zapytanie zaczyna się od **selektora labeli** `{label="value"}`, potem dodaje się **pipeline** — filtry, parsery, formatery. Filtr `|=` szuka tekstu, `|~` szuka regexem, `!=` wyklucza tekst.

## Zadanie
1. Znajdź wszystkie logi z błędami: `{service="app"} |= "error"`
2. Znajdź logi ostrzeżeń: `{service="app"} |= "warning"`
3. Wyklucz logi healthcheck: `{service="app"} != "/health"`
4. Policz ile błędów było w czasie — przełącz na tryb **Metric** (nad polem zapytania) i użyj: `count_over_time({service="app"} |= "error" [1m])`

<details>
<summary>Podpowiedź 1</summary>

`|=` to filtr "contains" — szuka tekstu w treści loga. Wielkość liter ma znaczenie. Użyj `|~ "(?i)error"` dla case-insensitive.

</details>

<details>
<summary>Podpowiedź 2</summary>

Przełącznik "Logs" / "Metric" jest nad polem zapytania w Explore. W trybie Metric, LogQL zwraca liczbę (jak PromQL) zamiast treści logów.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

```logql
# Logi z błędami
{service="app"} |= "error"

# Logi z ostrzeżeniami
{service="app"} |= "warning"

# Bez healthchecków
{service="app"} != "/health"

# Łączenie filtrów — błędy bez healthchecków
{service="app"} |= "error" != "/health"

# Zliczanie błędów per minuta (tryb Metric)
count_over_time({service="app"} |= "error" [1m])

# Rate błędów per sekunda
rate({service="app"} |= "error" [1m])
```

Jeśli nie widzisz błędów, uruchom symulację:
```bash
curl -X POST http://localhost:8000/simulate/errors
```
Poczekaj minutę, potem zresetuj: `curl -X POST http://localhost:8000/simulate/reset`

</details>
