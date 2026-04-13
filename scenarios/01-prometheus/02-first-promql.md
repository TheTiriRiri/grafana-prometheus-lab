# Scenariusz 2: Pierwsze zapytanie PromQL

## Cel
Nauczyć się wykonywać podstawowe zapytania PromQL i rozumieć wynik.

## Kontekst
**PromQL** (Prometheus Query Language) to język zapytań Prometheus. Każda metryka ma nazwę i zestaw **labeli** (etykiet) w formacie `nazwa{label1="val1", label2="val2"}`. Każda unikalna kombinacja nazwy i labeli to osobna **seria czasowa** (time series).

## Zadanie
1. Otwórz Prometheus UI: http://localhost:9090
2. W polu zapytania wpisz: `http_requests_total`
3. Kliknij **Execute**
4. Przełącz na zakładkę **Table** i **Graph**
5. Odpowiedz:
   - Ile serii czasowych widzisz?
   - Jakie labele mają te serie?
   - Dlaczego jest ich kilka, a nie jedna?

<details>
<summary>Podpowiedź 1</summary>

Każda unikalna kombinacja `method` + `endpoint` + `status` tworzy osobną serię. Np. `GET /products 200` i `GET /products 500` to dwie różne serie.

</details>

<details>
<summary>Podpowiedź 2</summary>

Spróbuj kliknąć na konkretną serię w tabeli — zobaczysz jej pełną nazwę z labelami.

</details>

<details>
<summary>Pokaż rozwiązanie</summary>

Zobaczysz wiele serii czasowych, np.:

```
http_requests_total{endpoint="/products", method="GET", status="200"} → 142
http_requests_total{endpoint="/products/1", method="GET", status="200"} → 87
http_requests_total{endpoint="/products/6", method="GET", status="404"} → 23
http_requests_total{endpoint="/orders", method="POST", status="200"} → 45
```

- **Labele:** `method` (GET/POST), `endpoint` (ścieżka URL), `status` (kod HTTP)
- Jest wiele serii, bo każda kombinacja labeli = osobna seria
- Wartość to **counter** — rośnie monotonnie, nigdy nie maleje (reset tylko przy restarcie)

W zakładce **Graph** widzisz jak counter rośnie w czasie — to jeszcze nie jest "ile requestów na sekundę", to surowa suma.

</details>
