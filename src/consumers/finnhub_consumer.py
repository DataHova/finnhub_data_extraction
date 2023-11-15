from confluent_kafka import Consumer, KafkaError
import socket
import logging
from core.logger import *
from core import config as config
log = Logger("Establishing Connection to the Kafka Producer...", logging.INFO).get_logger()

class KafkaConsumerWrapper:
    def __init__(self, conf, topic, message_callback=None):
        self.consumer = Consumer(conf)
        self.topic = topic
        self.message_callback = message_callback
        self.consumer.subscribe([self.topic])

    def _consume_message(self):
        msg = self.consumer.poll(1.0)
        if msg is None:
            # No message received in the polling interval
            return
        if msg.error():
            # Handle errors that occur while consuming
            if msg.error().code() == KafkaError._PARTITION_EOF:
                log.info("Reached end of partition")
            else:
                log.info("Error while consuming message:", msg.error())
        else:
            if self.message_callback:
                self.message_callback(msg)
            else:
                # Default behavior if no callback is provided
                log.info("Received message (key=%s, value=%s)" % (msg.key(), msg.value()))

    def consume_messages(self):
        try:
            while True:
                self._consume_message()
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()


def print_message(msg):
    print("Received message (key=%s, value=%s)" % (msg.key(), msg.value()))


if __name__ == "__main__":
    topic = config.topic
    group_id = config.group_id
    conf = {
        'bootstrap.servers': config.bootstrap_servers,
        'group.id': group_id,
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'client.id': socket.gethostname(),
        'auto.offset.reset': config.auto_offset_reset_earliest,
    }

    kafka_consumer = KafkaConsumerWrapper(conf, topic, message_callback=print_message)
    kafka_consumer.consume_messages()
