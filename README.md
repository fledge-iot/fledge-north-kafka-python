# fledge-north-kafka-python

Kafka is a distributed data streaming platform that makes a great north target for Fledge. This plugin acts as a Kafka Producer sending the data collected from Fledge to a topic. Once the data is in Kakfa, it may be processed and consumed by any number of additional processes. This provides great flexibility.

This plugin is a good example of a North plugin built in Python. There is also a Fledge North Kafka plugin written in C. You should compare the two to determine which one best meets your needs.

## Installation

Copy the python/fledge/plugins/north/kafka_python directory to /usr/local/fledge/python/fledge/python/plugins/north/
pip3 install -Ir python/requirements-kafka_python.txt

## Testing

Two test client applications are included in the test_clients directory. Set the BOOTSTRAP_SERVERS and KAFKA_TOPIC variables and you should be able to test the connection to your Kafka server.


