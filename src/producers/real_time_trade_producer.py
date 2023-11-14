from confluent_kafka import Producer
import socket
from finnhub_trade import FinnhubWebsocketClient

import os
from dotenv import load_dotenv
load_dotenv()
topic = os.getenv('topic')


conf = {'bootstrap.servers': 'localhost:9092',
        'client.id': socket.gethostname()}

producer = Producer(conf)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

msg = {
    "Type": "Key 2",
    "Name": "Sillians Basil",
    "Location": "San Francisco Bay Area",
    "Event": "Benz Events"
}


producer.produce(topic, key='hello', value=str(msg), callback=acked)
producer.flush(30)

