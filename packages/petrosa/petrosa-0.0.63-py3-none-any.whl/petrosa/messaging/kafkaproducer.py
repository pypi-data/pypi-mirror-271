import os

from kafka import KafkaProducer
import pkg_resources
import logging

ver = pkg_resources.get_distribution('petrosa').version
logging.info("petrosa-utils version: " + ver)



def get_producer():
    producer = KafkaProducer(bootstrap_servers=os.getenv(
        'KAFKA_ADDRESS', 'localhost:9092'),
                             client_id=os.getenv(
                                 "OTEL_SERVICE_NAME")
                             )

    return producer