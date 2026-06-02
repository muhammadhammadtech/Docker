#!/bin/bash

AB_FILE=~/lab104/results/ab_output.txt
SIEGE_FILE=~/lab104/results/siege_output.txt

echo "===== Performance Analysis ====="

echo ""
echo "[Apache Bench]"
RPS=$(grep "Requests per second" "$AB_FILE" | awk '{print $4}')
FAILED=$(grep "Failed requests" "$AB_FILE" | awk '{print $3}')
echo "Requests per second : $RPS"
echo "Failed requests     : $FAILED"

echo ""
echo "[Siege]"
TRANS_RATE=$(grep "transaction_rate" "$SIEGE_FILE" | awk -F: '{print $2}' | tr -d ' ,')
AVAILABILITY=$(grep "availability" "$SIEGE_FILE" | awk -F: '{print $2}' | tr -d ' ,')
echo "Transaction rate    : $TRANS_RATE"
echo "Availability        : $AVAILABILITY"

echo "================================"
