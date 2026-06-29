#!/bin/bash

AB_FILE=${AB_FILE:-"./results/ab_output.txt"}
SIEGE_FILE=${SIEGE_FILE:-"./results/siege_output.txt"}

echo "========== Performance Analysis =========="

# Verify benchmark files exist
for FILE in "$AB_FILE" "$SIEGE_FILE"; do
    if [ ! -f "$FILE" ]; then
        echo "Error: Benchmark file not found -> $FILE"
        exit 1
    fi
done

echo
echo "----- Apache Bench -----"

RPS=$(grep "Requests per second" "$AB_FILE" | awk '{print $4}')
FAILED=$(grep "Failed requests" "$AB_FILE" | awk '{print $3}')
TIME_PER_REQ=$(grep "Time per request" "$AB_FILE" | head -1 | awk '{print $4}')

echo "Requests/sec      : $RPS"
echo "Failed Requests   : $FAILED"
echo "Time per Request  : ${TIME_PER_REQ} ms"

echo
echo "----- Siege -----"

TRANS_RATE=$(grep "transaction_rate" "$SIEGE_FILE" | awk -F: '{print $2}' | tr -d ' ,')
AVAILABILITY=$(grep "availability" "$SIEGE_FILE" | awk -F: '{print $2}' | tr -d ' ,')
RESP_TIME=$(grep "response_time" "$SIEGE_FILE" | awk -F: '{print $2}' | tr -d ' ,')

echo "Transaction Rate  : $TRANS_RATE"
echo "Availability      : $AVAILABILITY"
echo "Response Time     : $RESP_TIME"

echo
echo "=========================================="
echo "Performance analysis completed successfully."
