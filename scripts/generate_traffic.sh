#!/bin/bash
# Skrypt generujący ruch do aplikacji FastAPI.
# Użycie: ./scripts/generate_traffic.sh
# Zatrzymanie: Ctrl+C

BASE_URL="http://localhost:8000"

echo "Generowanie ruchu do $BASE_URL ..."
echo "Naciśnij Ctrl+C aby zatrzymać."
echo ""

while true; do
    # Lista produktów
    curl -s "$BASE_URL/products" > /dev/null

    # Szczegóły produktu (id 1-7, gdzie 6-7 dadzą 404)
    PRODUCT_ID=$((RANDOM % 7 + 1))
    curl -s "$BASE_URL/products/$PRODUCT_ID" > /dev/null

    # Zamówienie (co 3. iteracja)
    if [ $((RANDOM % 3)) -eq 0 ]; then
        curl -s -X POST "$BASE_URL/orders" \
            -H "Content-Type: application/json" \
            -d "{\"product_id\": $((RANDOM % 5 + 1)), \"quantity\": $((RANDOM % 3 + 1))}" > /dev/null
    fi

    # Healthcheck (co 5. iteracja)
    if [ $((RANDOM % 5)) -eq 0 ]; then
        curl -s "$BASE_URL/health" > /dev/null
    fi

    # Losowy odstęp 0.1-0.5s
    sleep 0.$((RANDOM % 5 + 1))
done
