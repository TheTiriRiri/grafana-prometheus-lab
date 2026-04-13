# Scenariusz 6: Pierwszy panel

## Cel
Stworzyć pierwszy panel w Grafanie — wykres RPS w czasie.

## Kontekst
Grafana wizualizuje dane z Prometheusa jako **panele** w **dashboardach**. Panel to pojedynczy wykres/statystyka. Dashboard to zbiór paneli. Prometheus dostarczył dane, teraz trzeba je ładnie pokazać.

## Zadanie
1. Otwórz Grafanę: http://localhost:3000
2. Kliknij **+ → New dashboard → Add visualization**
3. Wybierz datasource **Prometheus**
4. W polu **Metric** wpisz zapytanie: `sum(rate(http_requests_total[1m])) by (endpoint)`
5. W polu **Legend** wpisz: `{{ endpoint }}`
6. Ustaw tytuł panelu: "Requests per Second"
7. Kliknij **Apply**
8. Zapisz dashboard jako "Mój pierwszy dashboard"

<details>
<summary>Podpowiedź 1</summary>

Pole metryki znajdziesz na dole panelu edycji. Przełącz z "Builder" na "Code" jeśli chcesz wpisać PromQL ręcznie.

</details>

<details>
<summary>Podpowiedź 2</summary>

`{{ endpoint }}` w Legend to szablon — Grafana zamieni go na wartość labela `endpoint` z każdej serii.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

1. **Dashboards → New → New dashboard → Add visualization**
2. Datasource: **Prometheus**
3. Przełącz na tryb **Code** (prawy górny róg edytora zapytań)
4. Wpisz: `sum(rate(http_requests_total[1m])) by (endpoint)`
5. Poniżej w **Options → Legend**: `{{ endpoint }}`
6. W prawym panelu u góry — wpisz tytuł: **Requests per Second**
7. Kliknij **Apply** (prawy górny róg)
8. Kliknij ikonę dyskietki (💾) → nazwa: "Mój pierwszy dashboard" → **Save**

Powinieneś widzieć wykres liniowy z osobną linią dla każdego endpointu.

</details>
