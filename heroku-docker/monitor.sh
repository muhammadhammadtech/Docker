#!/bin/bash
APP_URL=$1
echo "Monitoring application health..."
while true; do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${APP_URL}health)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    if [ "$RESPONSE" = "200" ]; then
        echo "[$TIMESTAMP] App is healthy (HTTP $RESPONSE)"
    else
        echo "[$TIMESTAMP] Issue detected (HTTP $RESPONSE)"
    fi
    sleep 30
done
