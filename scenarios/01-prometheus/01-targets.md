# Scenariusz 1: Poznaj targety

## Cel
Zrozumieć czym są targety w Prometheus i jak sprawdzić, czy zbieranie metryk działa.

## Kontekst
Prometheus działa w modelu **pull** — co określony czas (domyślnie 15s) odpytuje skonfigurowane endpointy (`/metrics`) i zapisuje pobrane metryki. Każdy taki endpoint to **target**. Jeśli target ma status UP, oznacza to, że Prometheus poprawnie pobiera z niego metryki.

## Zadanie
1. Otwórz Prometheus UI: http://localhost:9090
2. Przejdź do **Status → Targets**
3. Odpowiedz na pytania:
   - Ile targetów jest skonfigurowanych?
   - Jakie to targety (nazwy jobów)?
   - Co oznacza status **UP**?
   - Jaki jest interwał scrapowania (scrape interval)?

<details>
<summary>Podpowiedź 1</summary>

Strona Targets pokazuje tabelę z kolumnami: Endpoint, State, Labels, Last Scrape, Scrape Duration, Error.

</details>

<details>
<summary>Podpowiedź 2</summary>

Nazwy jobów odpowiadają sekcjom `job_name` w pliku `prometheus/prometheus.yml`.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**3 targety:**

| Job | Target | Opis |
|-----|--------|------|
| `prometheus` | `localhost:9090` | Sam Prometheus monitoruje siebie |
| `fastapi-app` | `app:8000` | Nasza aplikacja sklepu |
| `node-exporter` | `node-exporter:9100` | Metryki systemowe hosta |

- **UP** oznacza, że Prometheus może się połączyć z targetem i pobrać metryki
- **Scrape interval** to 15s (ustawione w `global.scrape_interval` w `prometheus.yml`)

Warto też kliknąć na endpoint targetu (np. `http://app:8000/metrics`) — zobaczysz surowe metryki w formacie tekstowym Prometheus.

</details>
