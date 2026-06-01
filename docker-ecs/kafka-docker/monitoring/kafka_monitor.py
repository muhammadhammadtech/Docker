#!/usr/bin/env python3
import subprocess
from datetime import datetime

class KafkaMonitor:
    def __init__(self, kafka_container='kafka-broker'):
        self.kafka_container = kafka_container

    def get_topic_info(self):
        cmd = f"docker exec {self.kafka_container} kafka-topics --bootstrap-server localhost:9092 --describe"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        return result.stdout

    def get_consumer_groups(self):
        cmd = f"docker exec {self.kafka_container} kafka-consumer-groups --bootstrap-server localhost:9092 --list"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        return result.stdout.strip().split('\n')

    def get_consumer_group_details(self, group_id):
        cmd = f"docker exec {self.kafka_container} kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group {group_id}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        return result.stdout

    def monitor_cluster(self):
        print(f"=== Kafka Cluster Monitor - {datetime.now()} ===")
        print("\n--- Topic Information ---")
        print(self.get_topic_info())
        print("\n--- Consumer Groups ---")
        groups = self.get_consumer_groups()
        for group in groups:
            if group.strip():
                print(f"\nGroup: {group}")
                print(self.get_consumer_group_details(group))

if __name__ == "__main__":
    monitor = KafkaMonitor()
    monitor.monitor_cluster()
