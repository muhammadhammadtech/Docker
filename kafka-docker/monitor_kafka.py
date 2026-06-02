#!/usr/bin/env python3

import subprocess
import time
from datetime import datetime

def get_container_stats():
    try:
        result = subprocess.run(
            ['docker', 'stats', 'kafka', '--no-stream', '--format',
             'table {{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}'],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error getting stats: {e}"

def get_kafka_topics():
    try:
        result = subprocess.run(
            ['docker', 'exec', 'kafka', 'kafka-topics', '--list',
             '--bootstrap-server', 'localhost:9092'],
            capture_output=True, text=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Error: {e}"]

def get_topic_details(topic):
    try:
        result = subprocess.run(
            ['docker', 'exec', 'kafka', 'kafka-topics', '--describe',
             '--topic', topic, '--bootstrap-server', 'localhost:9092'],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Kafka Monitoring Dashboard")
    print("=" * 50)

    while True:
        try:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

            print("\n--- Container Statistics ---")
            print(get_container_stats())

            print("\n--- Topics ---")
            topics = get_kafka_topics()
            for topic in topics:
                if topic and not topic.startswith('Error'):
                    print(f"Topic: {topic}")

            if 'test-messages' in topics:
                print("\n--- test-messages Topic Details ---")
                print(get_topic_details('test-messages'))

            print("\n" + "=" * 50)
            time.sleep(10)

        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
