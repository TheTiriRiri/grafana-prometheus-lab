# Scenariusz 14: Dashboard z logami

## Cel
Dodać panel z logami do dashboardu obok metryk.

## Kontekst
Grafana pozwala mieszać panele z różnych datasource'ów na jednym dashboardzie. Panel typu **Logs** pokazuje logi z Loki. Umieszczony obok paneli z metrykami (Prometheus) daje pełny obraz: widzisz CO się dzieje (metryki) i DLACZEGO (logi).

## Zadanie
1. Otwórz dashboard "Application Overview"
2. Dodaj nowy panel typu **Logs**
3. Datasource: **Loki**
4. Zapytanie: `{service="app"} | json | level="error"`
5. Ustaw tytuł: "Application Errors"
6. Umieść go pod istniejącymi panelami
7. Użyj split view w Explore — otwórz metryki i logi obok siebie

<details>
<summary>Podpowiedź 1</summary>

Typ panelu "Logs" znajdziesz w dropdownie typów. Wyświetla logi w formie listy z timestampem.

</details>

<details>
<summary>Podpowiedź 2</summary>

Split view w Explore: kliknij przycisk "Split" (prawy górny róg Explore). Lewa strona — Prometheus, prawa — Loki. Oba dzielą ten sam zakres czasu.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Panel Logs na dashboardzie:**
1. Dashboard → Add visualization
2. Datasource: **Loki**
3. Zapytanie (Code mode): `{service="app"} | json | level=~"error|warning"`
4. Typ panelu: **Logs**
5. Tytuł: "Application Errors & Warnings"
6. Apply → przeciągnij panel na dół dashboardu
7. Save dashboard

**Split view w Explore:**
1. Explore (kompas) → datasource: Prometheus
2. Zapytanie: `sum(rate(http_requests_total{status=~"5.."}[1m]))`
3. Kliknij **Split** (prawy górny róg)
4. W prawym panelu: datasource: **Loki**
5. Zapytanie: `{service="app"} | json | level="error"`

Teraz widzisz metryki i logi obok siebie z tym samym zakresem czasu.

</details>
