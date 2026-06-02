#!/bin/bash
echo "=== Kafka Performance Monitor ==="
echo "Timestamp: $(date)"
echo
echo "--- Container Resource Usage ---"
docker stats --no-stream kafka-broker kafka-zookeeper kafka-producer kafka-consumer 2>/dev/null
echo
echo "--- Kafka Broker Logs (Last 10 lines) ---"
docker logs --tail 10 kafka-broker
echo
echo "--- Topic Partition Details ---"
docker exec kafka-broker kafka-topics --bootstrap-server localhost:9092 --describe
echo
echo "--- Consumer Group Status ---"
GROUPS=$(docker exec kafka-broker kafka-consumer-groups --bootstrap-server localhost:9092 --list 2>/dev/null)
if [ -n "$GROUPS" ]; then
    for group in $GROUPS; do
        echo "Group: $group"
        docker exec kafka-broker kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group $group
        echo
    done
fi
