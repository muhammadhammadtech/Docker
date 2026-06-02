#!/bin/bash
APP_URL=$1
echo "Starting load test for $APP_URL"
for i in {1..50}; do
    curl -s $APP_URL > /dev/null &
    curl -s ${APP_URL}health > /dev/null &
    curl -s ${APP_URL}api/info > /dev/null &
    curl -s ${APP_URL}api/env > /dev/null &
    if [ $((i % 10)) -eq 0 ]; then
        echo "Completed $i iterations"
    fi
done
wait
echo "Load test completed"
