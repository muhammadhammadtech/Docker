#!/bin/bash
echo "=== Autoscaling Verification ==="

echo "1. Checking HPA..."
if kubectl get hpa web-app-hpa &>/dev/null; then
    echo "HPA is configured"
    kubectl get hpa web-app-hpa
else
    echo "HPA not found"
    exit 1
fi

echo
echo "2. Current pod count..."
CURRENT_PODS=$(kubectl get pods -l app=web-app --no-headers | wc -l)
echo "Pod count: $CURRENT_PODS"

echo
echo "3. Checking metrics..."
if kubectl top pods -l app=web-app &>/dev/null; then
    echo "Metrics available"
    kubectl top pods -l app=web-app
else
    echo "Metrics not ready yet (normal initially)"
fi

echo
echo "4. Checking service..."
if kubectl get service web-app-service &>/dev/null; then
    echo "Service is up"
    kubectl get service web-app-service
else
    echo "Service not found"
fi

echo
echo "=== Done ==="
