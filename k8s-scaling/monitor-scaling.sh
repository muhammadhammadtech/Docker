#!/bin/bash
echo "=== Kubernetes Autoscaling Monitor ==="
echo "Press Ctrl+C to stop"
while true; do
    clear
    echo "=== Time: $(date) ==="
    echo
    echo "--- HPA Status ---"
    kubectl get hpa web-app-hpa
    echo
    echo "--- Pod Count ---"
    kubectl get pods -l app=web-app -o wide
    echo
    echo "--- Resource Usage ---"
    kubectl top pods -l app=web-app 2>/dev/null || echo "Metrics not ready yet..."
    echo
    sleep 10
done
