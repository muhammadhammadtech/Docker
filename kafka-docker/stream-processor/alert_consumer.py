#!/usr/bin/env python3
import json, logging
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'sensor-alerts',
            bootstrap_servers=['kafka:29092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            group_id='alert-consumer-group',
            auto_offset_reset='earliest'
        )

    def handle_alert(self, alert):
        alert_type = alert.get('alert_type')
        sensor_id = alert.get('sensor_id')
        location = alert.get('location')
        severity = alert.get('severity')
        current_value = alert.get('current_value')
        threshold = alert.get('threshold')

        if severity == 'HIGH':
            logger.error(f"🚨 CRITICAL ALERT: {alert_type} at {location}")
            logger.error(f"   Sensor: {sensor_id}, Current Value: {current_value}, Threshold: {threshold}")
        elif severity == 'MEDIUM':
            logger.warning(f"⚠️  WARNING: {alert_type} at {location}")
            logger.warning(f"   Sensor: {sensor_id}, Current Value: {current_value}")

    def start_consuming(self):
        logger.info("Starting alert consumer...")
        try:
            for message in self.consumer:
                self.handle_alert(message.value)
        except KeyboardInterrupt:
            logger.info("Alert consumer interrupted")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    consumer = AlertConsumer()
    consumer.start_consuming()
