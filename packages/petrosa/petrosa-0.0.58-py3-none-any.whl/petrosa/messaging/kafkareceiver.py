import os

from kafka import KafkaConsumer
import pkg_resources
import logging

ver = pkg_resources.get_distribution('petrosa').version
logging.info("petrosa-utils version: " + ver)



def get_consumer(topic) -> KafkaConsumer:
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=os.getenv(
                                 'KAFKA_SUBSCRIBER', 'localhost:9093'),
                             group_id=os.getenv(
                                 "OTEL_SERVICE_NAME")
                             )

    return consumer