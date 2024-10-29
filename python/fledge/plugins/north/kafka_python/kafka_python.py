# -*- coding: utf-8 -*-

"""Kafka North plugin"""
import asyncio
import json
import numpy as np

from kafka import KafkaProducer
from kafka.errors import KafkaError

from fledge.common import logger
from fledge.plugins.north.common.common import *

__author__ = "Rob Raesemann"
__copyright__ = "Copyright (c) 2020 Raesemann Enterprises"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

_LOGGER = logger.setup(__name__)

_DEFAULT_CONFIG = {
    'plugin': {
         'description': 'Kafka North Plugin',
         'type': 'string',
         'default': 'kafka_python',
         'readonly': 'true'
    },
    'bootstrap_servers': {
        'description': 'Kafka Bootstrap Server',
        'type': 'string',
        'default': 'localhost:9092',
        'order': '1',
        'displayName': 'Boostrap Server'
    },
    'kafka_topic': {
        'description': 'Kafka Topic',
        'type': 'string',
        'default': 'iot-readings',
        'order': '2',
        'displayName': 'Kafka Topic'
    },
    "source": {
         "description": "Source of data to be sent on the stream. May be either readings or statistics.",
         "type": "enumeration",
         "default": "readings",
         "options": ["readings", "statistics"],
         'order': '3',
         'displayName': 'Source'
    }
}


def plugin_info():
    return {
        'name': 'kafka_north_python',
        'version': '2.6.0',
        'type': 'north',
        'interface': '1.0',
        'config': _DEFAULT_CONFIG
    }


def plugin_init(data):
    global kafka_north, config
    kafka_north = KafkaNorthPlugin()
    config = data
    return config


async def plugin_send(data, payload, stream_id):
    try:
        is_data_sent, new_last_object_id, num_sent = await kafka_north.send_payloads(payload)
    except asyncio.CancelledError:
        pass
    else:
        return is_data_sent, new_last_object_id, num_sent


def plugin_shutdown(data):
    pass


def plugin_reconfigure():
    pass


class KafkaNorthPlugin(object):
    """ North Kafka Plugin """

    def __init__(self):
        self.event_loop = asyncio.get_event_loop()

    def kafka_error(self, error):
        _LOGGER.error(f'Kafka error: {error}')

    async def send_payloads(self, payloads):
        is_data_sent = False
        last_object_id = 0
        num_sent = 0
        try:
            payload_block = list()
            for p in payloads:
                read = dict()
                read["asset"] = p['asset_code']
                last_object_id = p["id"]
                for k, v in p['reading'].items():
                    if not isinstance(v, np.ndarray):
                        read["readings"] = p['reading']
                read["timestamp"] = p['user_ts']
                payload_block.append(read)
            num_sent = await self._send_payloads(payload_block)
            is_data_sent = True
        except Exception as ex:
            _LOGGER.exception(ex, "Data could not be sent!")
        return is_data_sent, last_object_id, num_sent

    async def _send_payloads(self, payload_block):
        """ send a list of block payloads"""
        num_count = 0
        try:
            producer = KafkaProducer(bootstrap_servers=config["bootstrap_servers"]["value"],
                                     api_version=(0, 11), value_serializer=lambda x: json.dumps(x).encode('utf-8'))
            await self._send(producer, payload_block)
        except Exception as ex:
            _LOGGER.exception(f'Exception sending payloads: {ex}')
        else:
            num_count += len(payload_block)
        return num_count

    async def _send(self, producer, payload):
        """ Send the payload, using provided producer """
        producer.send(config["kafka_topic"]["value"], value=payload).add_errback(self.kafka_error)
        producer.flush()
