from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
import sys

BOOTSTRAP_SERVERS = ['3.209.55.41:9092']
KAFKA_TOPIC = 'foglamp-testing'


_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
_LOGGER.addHandler(handler)

consumer = KafkaConsumer(KAFKA_TOPIC, 
                        auto_offset_reset='earliest',
                        bootstrap_servers=BOOTSTRAP_SERVERS, 
                        api_version=(0,11),
                        consumer_timeout_ms=1000)

_LOGGER.info(f'Waiting for messages from topic: {KAFKA_TOPIC}')

for msg in consumer:
    _LOGGER.info (f'message: {msg}')

_LOGGER.info('Done')