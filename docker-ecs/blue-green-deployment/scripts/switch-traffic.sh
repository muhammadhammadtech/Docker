#!/bin/bash

set -e

TARGET_ENV=${1:-blue}

echo "=== Traffic Switching Script ==="
echo "Switching traffic to: $TARGET_ENV"
echo "==============================="

if [ "$TARGET_ENV" != "blue" ] && [ "$TARGET_ENV" != "green" ]; then
    echo "Error: Environment must be 'blue' or 'green'"
    exit 1
fi

cp nginx/conf/nginx-$TARGET_ENV.conf nginx/conf/nginx.conf

docker exec nginx-lb nginx -s reload

echo "Traffic switched to $TARGET_ENV environment"

sleep 2
RESPONSE=$(curl -s http://localhost | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['environment'])" 2>/dev/null || echo "Could not parse response")
echo "Current active environment: $RESPONSE"
