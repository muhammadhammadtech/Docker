#!/bin/bash

BLUE_URL="http://localhost:3001/health"
GREEN_URL="http://localhost:3002/health"
LB_URL="http://localhost/health"

echo "=== Health Monitoring ==="
echo "Timestamp: $(date)"
echo "========================"

echo -n "Blue Environment: "
if curl -f -s $BLUE_URL > /dev/null 2>&1; then
    echo "HEALTHY"
else
    echo "UNHEALTHY"
fi

echo -n "Green Environment: "
if curl -f -s $GREEN_URL > /dev/null 2>&1; then
    echo "HEALTHY"
else
    echo "UNHEALTHY"
fi

echo -n "Load Balancer: "
if curl -f -s $LB_URL > /dev/null 2>&1; then
    echo "HEALTHY"
else
    echo "UNHEALTHY"
fi

echo "========================"
