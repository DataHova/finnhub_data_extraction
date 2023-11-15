from confluent_kafka import Producer
import socket
from finnhub_trade import FinnhubWebsocketClient
from core.logger import *
from core import config as config
import logging
log = Logger("Establishing Connection to the Finnhub websocket...", logging.INFO).get_logger()

class KafkaProducerWrapper:
    def __init__(self, conf, topic):
        self.producer = Producer(conf)
        self.topic = topic

    def acked(self, err, msg):
        if err is not None:
            log.info("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            log.info("Message produced: %s" % (str(msg)))

    def produce_message(self, message):
        self.producer.produce(self.topic, value=message, callback=self.acked)

    def flush(self, timeout):
        self.producer.flush(timeout)


class EnhancedFinnhubClient(FinnhubWebsocketClient):
    def __init__(self, api_key, on_message_callback=None, ticker_filepath='tickers.yml'):
        super().__init__(api_key, ticker_filepath)
        self.on_message_callback = on_message_callback

    def on_message(self, ws, message):
        if self.on_message_callback:
            self.on_message_callback(message)
        print("Received message:", message)


if __name__ == "__main__":
    # Kafka Setup
    topic = config.topic
    conf = {
        'bootstrap.servers': config.bootstrap_servers,
        'client.id': socket.gethostname()
    }
    kafka_producer = KafkaProducerWrapper(conf, topic)

    # Finnhub client setup
    FINNHUB_API_KEY = config.finnhub_api_key
    client = EnhancedFinnhubClient(FINNHUB_API_KEY, kafka_producer.produce_message)
    client.run()

    kafka_producer.flush(30)

