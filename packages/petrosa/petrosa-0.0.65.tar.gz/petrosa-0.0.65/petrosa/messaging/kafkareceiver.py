import os

from kafka import KafkaConsumer
import pkg_resources
import logging
import retry

ver = pkg_resources.get_distribution('petrosa').version
logging.info("petrosa-utils version: " + ver)


@retry.retry(tries=5, backoff=2, logger=logging.getLogger(__name__))
def get_consumer(topic) -> KafkaConsumer:
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=os.getenv(
                                 'KAFKA_SUBSCRIBER', 'localhost:9093'),
                             group_id=os.getenv(
                                 "OTEL_SERVICE_NAME")
                             )

    return consumer