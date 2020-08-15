from kafka import KafkaProducer
import json
import logging


class KafkaObj(object):
    _topic = None
    _server = None
    _producer = None

    def __init__(self, server, topic,
                 value_serializer=lambda m: json.dumps(m).encode()):
        self._server = server
        self._topic = topic
        self._producer = KafkaProducer(bootstrap_servers=server,
                                       value_serializer=value_serializer)

    def getTopic(self):
        return self._topic

    def setTopic(self, topic):
        self._topic = topic

    def send(self, msg):
        try:
            self._producer.send(self._topic, msg)
            return 200
        except Exception as e:
            logging.error("ERROR: write kafka error：{}".format(e))
            return 9092
