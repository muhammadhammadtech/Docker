#!/bin/bash
echo "=== Kafka Log Monitor ==="
for service in kafka-broker kafka-zookeeper kafka-producer kafka-consumer; do
    echo "Monitoring logs for $service..."
    timeout 10 docker logs -f --tail 20 $service 2>&1
    echo
done
echo "Log monitoring complete."
