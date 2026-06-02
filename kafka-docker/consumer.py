#!/usr/bin/env python3

import json
from kafka import KafkaConsumer
from datetime import datetime

def create_consumer():
    consumer = KafkaConsumer(
        'test-messages',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        group_id='test-consumer-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    return consumer

def main():
    consumer = create_consumer()

    print("Starting consumer...")
    print("Waiting for messages (Press Ctrl+C to stop)")

    try:
        message_count = 0
        for message in consumer:
            message_count += 1
            print(f"\n--- Message {message_count} ---")
            print(f"Topic: {message.topic}")
            print(f"Partition: {message.partition}")
            print(f"Offset: {message.offset}")
            print(f"Key: {message.key}")
            print(f"Value: {message.value}")
            print(f"Timestamp: {datetime.fromtimestamp(message.timestamp/1000)}")
    except KeyboardInterrupt:
        print(f"\nStopping consumer. Total messages processed: {message_count}")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
