# Scenariusz 13: LogQL — parsowanie

## Cel
Wyciągnąć pola z JSON logów i tworzyć metryki z logów.

## Kontekst
Nasze logi to JSON. LogQL potrafi je sparsować operatorem `| json` — każde pole JSON staje się labelem, którego można użyć do filtrowania. To potężne narzędzie: zamiast szukać tekstu "error", możesz filtrować po `level="error"` — precyzyjnie.

## Zadanie
1. Sparsuj JSON logi: `{service="app"} | json`
2. Filtruj po sparsowanym polu: `{service="app"} | json | level="error"`
3. Wyciągnij request_id z błędów: `{service="app"} | json | level="error" | line_format "{{.request_id}} — {{.event}}"`
4. Stwórz metrykę — ile requestów per endpoint (tryb Metric): `sum by (endpoint)(count_over_time({service="app"} | json | endpoint!="" [1m]))`

<details>
<summary>Podpowiedź 1</summary>

Po `| json` masz dostęp do wszystkich pól z JSONa jako labeli. Sprawdź jakie pola są dostępne rozwijając log po sparsowaniu.

</details>

<details>
<summary>Podpowiedź 2</summary>

`| line_format` zmienia format wyświetlanego loga. Używa składni Go templates: `{{.nazwa_pola}}`.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

```logql
# Parsowanie JSON — każde pole staje się labelem
{service="app"} | json

# Filtrowanie po sparsowanym polu level
{service="app"} | json | level="error"

# Tylko określone pola w output
{service="app"} | json | level="error" | line_format "{{.request_id}} — {{.event}}"

# Metryka: requesty per endpoint (Metric mode)
sum by (endpoint)(count_over_time({service="app"} | json | endpoint!="" [1m]))

# Metryka: requesty per level
sum by (level)(count_over_time({service="app"} | json [1m]))
```

`| json` + filtrowanie po labelach to najpotężniejsza kombinacja w LogQL. Pozwala na precyzyjne wyszukiwanie bez skanowania tekstu.

</details>
