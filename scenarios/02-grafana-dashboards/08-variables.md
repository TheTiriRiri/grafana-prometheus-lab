# Scenariusz 8: Zmienne (variables)

## Cel
Dodać interaktywny dropdown do dashboardu, który filtruje dane po endpoincie.

## Kontekst
Zmienne (template variables) w Grafanie pozwalają na tworzenie dynamicznych dashboardów. Zamiast tworzyć osobny panel dla każdego endpointu, tworzysz jeden dashboard z dropdownem. Zmienna jest dostępna w zapytaniach jako `$nazwa_zmiennej`.

## Zadanie
1. Otwórz dashboard "Application Overview"
2. Wejdź w ustawienia dashboardu (ikona koła zębatego)
3. Przejdź do zakładki **Variables** → **New variable**
4. Stwórz zmienną `endpoint` typu **Query** z Prometheusa
5. Użyj zmiennej w zapytaniach paneli (dodaj filtr `{endpoint="$endpoint"}`)
6. Sprawdź czy dropdown działa — zmień wartość i obserwuj panele

<details>
<summary>Podpowiedź 1</summary>

Zapytanie dla zmiennej, które zwraca wszystkie wartości labela `endpoint`:

```
label_values(http_requests_total, endpoint)
```

</details>

<details>
<summary>Podpowiedź 2</summary>

Zaznacz opcję "Include All option" żeby mieć możliwość wybrania wszystkich endpointów naraz. Ustaw też "Multi-value" aby móc wybrać kilka.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Tworzenie zmiennej:**
1. Dashboard Settings (⚙️) → Variables → New variable
2. Name: `endpoint`
3. Type: **Query**
4. Data source: **Prometheus**
5. Query: `label_values(http_requests_total, endpoint)`
6. Multi-value: ✅
7. Include All option: ✅
8. Click **Apply** → **Save dashboard**

**Użycie zmiennej w panelu RPS:**
Zmień zapytanie z:
```promql
sum(rate(http_requests_total[1m])) by (endpoint)
```
na:
```promql
sum(rate(http_requests_total{endpoint=~"$endpoint"}[1m])) by (endpoint)
```

Użyj `=~` (regex match) zamiast `=`, bo przy Multi-value Grafana generuje regex `val1|val2|val3`.

Powtórz dla pozostałych paneli.

</details>
