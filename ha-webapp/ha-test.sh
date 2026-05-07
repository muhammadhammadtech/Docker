#!/bin/bash

echo "=== Starting High Availability Test ==="

test_availability() {
    local label=$1
    echo ""
    echo "--- Testing: $label ---"
    for i in {1..8}; do
        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
        if [ "$response" = "200" ]; then
            echo "  Request $i: SUCCESS (HTTP 200)"
        else
            echo "  Request $i: FAILED (HTTP $response)"
        fi
        sleep 1
    done
}

test_availability "Normal Operation"

echo ""
echo "Killing a container to simulate failure..."
CONTAINER_ID=$(sudo docker ps --format "{{.ID}}\t{{.Image}}" | grep ha-webapp | head -1 | awk '{print $1}')
sudo docker kill $CONTAINER_ID
sleep 5

test_availability "After Container Kill"

echo ""
echo "Scaling down to 2 replicas..."
sudo docker service scale webapp-stack_web=2
sleep 10
test_availability "After Scale Down"

echo ""
echo "Scaling up to 4 replicas..."
sudo docker service scale webapp-stack_web=4
sleep 10
test_availability "After Scale Up"

echo ""
echo "=== HA Test Complete ==="
