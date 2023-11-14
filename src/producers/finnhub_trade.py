import websocket
from websocket._app import WebSocketApp
from websocket._logging import enableTrace
import yaml
import os
from dotenv import load_dotenv

class FinnhubWebsocketClient:
    def __init__(self, api_key, ticker_filepath='tickers.yml'):
        self.api_key = api_key
        self.ticker_filepath = ticker_filepath
        self.ws = None
        self._setup_websocket()

    def _setup_websocket(self):
        enableTrace(True)
        self.ws = WebSocketApp(f"wss://ws.finnhub.io?token={self.api_key}",
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.on_open = self.on_open

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def load_subscriptions_from_yaml(self):
        with open(self.ticker_filepath, 'r') as file:
            data = yaml.safe_load(file)
        return data.get('subscriptions', [])

    def on_open(self, ws):
        subscriptions = self.load_subscriptions_from_yaml()
        for symbol in subscriptions:
            command = '{"type":"subscribe","symbol":"%s"}' % symbol
            print('Successfully opened a connection!')
            ws.send(command)

    def run(self):
        self.ws.run_forever()

if __name__ == "__main__":
    load_dotenv()
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    client = FinnhubWebsocketClient(FINNHUB_API_KEY)
    client.run()
