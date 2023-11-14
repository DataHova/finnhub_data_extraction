from confluent_kafka import Consumer, KafkaError
import socket
import os

from dotenv import load_dotenv
load_dotenv()


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
                print("Reached end of partition")
            else:
                print("Error while consuming message:", msg.error())
        else:
            if self.message_callback:
                self.message_callback(msg)
            else:
                # Default behavior if no callback is provided
                print("Received message (key=%s, value=%s)" % (msg.key(), msg.value()))

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
    topic = os.getenv('topic')
    group_id = os.getenv('groupid')
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': group_id,
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'client.id': socket.gethostname(),
        'auto.offset.reset': 'earliest',
    }

    kafka_consumer = KafkaConsumerWrapper(conf, topic, message_callback=print_message)
    kafka_consumer.consume_messages()
