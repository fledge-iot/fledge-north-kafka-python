# fledge-north-kafka-python

Kafka is a distributed data streaming platform that makes a great north target for Fledge. This plugin acts as a Kafka Producer sending the data collected from Fledge to a topic. Once the data is in Kakfa, it may be processed and consumed by any number of additional processes. This provides great flexibility.

This plugin is a good example of a North plugin built in Python. There is also a Fledge North Kafka plugin written in C. You should compare the two to determine which one best meets your needs.

## Installation

pip install requirements.txt

Create a directory called kafka_north for your plugin  
  
/usr/local/fledge/python/foglamp/python/plugins/north/kafka_north

Copy the __init__.py and kafka_north.py files to /usr/local/foglamp/python/foglamp/python/plugins/north/kafka_north.py


## Testing
Two test client applications are included in the test_clients directory. Set the BOOTSTRAP_SERVERS and KAFKA_TOPIC variables and you should be able to test the connection to your Kafka server.


