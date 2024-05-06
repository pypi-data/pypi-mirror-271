import os

from kafka import KafkaProducer
import pkg_resources
import logging
import retry


ver = pkg_resources.get_distribution('petrosa').version
logging.info("petrosa-utils version: " + ver)


@retry.retry(tries=5, backoff=2, logger=logging.getLogger(__name__))
def get_producer():
    producer = KafkaProducer(bootstrap_servers=os.getenv(
        'KAFKA_ADDRESS', 'localhost:9092'),
                             client_id=os.getenv(
                                 "OTEL_SERVICE_NAME")
                             )

    return producer
