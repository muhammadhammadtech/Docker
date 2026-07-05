#!/bin/bash

APP_URL="$1"
INTERVAL="${2:-30}"
LOG_FILE="./monitor.log"

if [ -z "$APP_URL" ]; then
    echo "Usage: $0 <app-url> [interval]"
    echo "Example: ./monitor.sh https://my-app.herokuapp.com/ 15"
    exit 1
fi

trap 'echo -e "\nMonitoring stopped."; exit 0' SIGINT

echo "========================================"
echo "Starting application health monitoring"
echo "Target   : ${APP_URL}health"
echo "Interval : ${INTERVAL}s"
echo "Log File : $LOG_FILE"
echo "========================================"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    RESPONSE=$(curl \
        --silent \
        --output /dev/null \
        --write-out "%{http_code}" \
        --max-time 5 \
        "${APP_URL}health")

    if [ "$RESPONSE" = "200" ]; then
        MESSAGE="[$TIMESTAMP] Healthy (HTTP $RESPONSE)"
    else
        MESSAGE="[$TIMESTAMP] Unhealthy (HTTP $RESPONSE)"
    fi

    echo "$MESSAGE" | tee -a "$LOG_FILE"

    sleep "$INTERVAL"
done
