#!/usr/bin/env python3
import json
import os
import time
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
from datetime import datetime
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(",")
TOPIC = os.getenv("KAFKA_TOPIC", "test-messages")
SEND_INTERVAL = float(os.getenv("SEND_INTERVAL_SECONDS", "2"))


def create_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        acks="all",
        retries=5,
        retry_backoff_ms=300,
    )


def generate_sample_data():
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": random.randint(1000, 9999),
        "action": random.choice(["login", "logout", "purchase", "view"]),
        "value": round(random.uniform(10.0, 1000.0), 2),
    }


def on_send_success(record_metadata, count):
    logger.info(
        "Message #%d → topic=%s partition=%d offset=%d",
        count, record_metadata.topic, record_metadata.partition, record_metadata.offset,
    )


def on_send_error(exc, count):
    logger.error("Message #%d failed: %s", count, exc)


def main():
    producer = create_producer()
    logger.info("Producer started → topic: %s | brokers: %s", TOPIC, BOOTSTRAP_SERVERS)
    logger.info("Press Ctrl+C to stop")

    message_count = 0
    try:
        while True:
            data = generate_sample_data()
            key = f"user_{data['user_id']}"
            message_count += 1
            (
                producer.send(TOPIC, key=key, value=data)
                .add_callback(on_send_success, message_count)
                .add_errback(on_send_error, message_count)
            )
            logger.info("Queued message #%d: %s", message_count, data)
            time.sleep(SEND_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Stopping producer. Messages queued: %d", message_count)
    finally:
        producer.flush()
        producer.close()
        logger.info("Producer closed cleanly.")


if __name__ == "__main__":
    main()
