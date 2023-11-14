import websocket
from websocket._app import WebSocketApp
from websocket._logging import enableTrace
import yaml

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

def on_message(ws, message):
    print(message)
    

def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def load_subscriptions_from_yaml(filepath):
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('subscriptions', [])


def on_open(ws):
    subscriptions = load_subscriptions_from_yaml('tickers.yml')
    
    for symbol in subscriptions:
        command = '{"type":"subscribe","symbol":"%s"}' % symbol
        print('Succesfully opened a connection!')
        ws.send(command)
        

if __name__ == "__main__":
    enableTrace(True)
    ws = WebSocketApp(f"wss://ws.finnhub.io?token={FINNHUB_API_KEY}",
                      on_message = on_message,
                      on_error = on_error,
                      on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()