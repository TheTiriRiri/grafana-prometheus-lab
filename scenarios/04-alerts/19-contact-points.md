# Scenariusz 19: Contact points i silence

## Cel
Skonfigurować gdzie wysyłać powiadomienia i nauczyć się wyciszać alerty.

## Kontekst
**Contact point** to miejsce, gdzie trafiają powiadomienia z alertów (email, Slack, webhook). **Notification policy** decyduje który alert trafia do którego contact pointu. **Silence** pozwala tymczasowo wyciszyć alert (np. podczas planowanego maintenance).

## Zadanie
1. Stwórz contact point typu **Webhook** (nie wymaga zewnętrznych serwisów)
2. Skonfiguruj notification policy aby alerty z folderu "App Alerts" szły do tego webhooka
3. Naucz się wyciszać alert (Silence)

<details>
<summary>Podpowiedź 1</summary>

Webhook contact point: użyj `http://app:8000/health` jako URL (użyj nazwy Docker service, nie localhost — Grafana działa wewnątrz sieci Docker). W prawdziwym scenariuszu byłby to Slack webhook, PagerDuty, itp.

</details>

<details>
<summary>Podpowiedź 2</summary>

Silence: Alerting → Silences → New silence. Ustaw czas trwania i matcher (np. folder="App Alerts").

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

**Contact point (Webhook):**
1. Alerting → Contact points → New contact point
2. Name: "Test Webhook"
3. Integration: **Webhook**
4. URL: `http://app:8000/health` (użyj nazwy Docker service, nie localhost)
5. Test → Send test notification
6. Save

**Notification policy:**
1. Alerting → Notification policies
2. New nested policy
3. Matcher: `grafana_folder = App Alerts`
4. Contact point: "Test Webhook"
5. Save

**Silence:**
1. Alerting → Silences → New silence
2. Duration: 1h
3. Label matcher: `alertname = High Error Rate`
4. Comment: "Planowany maintenance"
5. Submit

Silence wygasa automatycznie po ustawionym czasie. Możesz też ręcznie go zakończyć wcześniej (Expire).

</details>
