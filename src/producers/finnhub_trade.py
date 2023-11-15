import websocket
from websocket._app import WebSocketApp
from websocket._logging import enableTrace
import yaml
from core.logger import *
from core import config as config
import logging
log = Logger("Helper Script for kafka Producer...", logging.INFO).get_logger()

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
        log.info(message)

    def on_error(self, ws, error):
        log.info(error)

    def on_close(self, ws):
        log.info("### closed ###")

    def load_subscriptions_from_yaml(self):
        with open(self.ticker_filepath, 'r') as file:
            data = yaml.safe_load(file)
        return data.get('subscriptions', [])

    def on_open(self, ws):
        subscriptions = self.load_subscriptions_from_yaml()
        for symbol in subscriptions:
            command = '{"type":"subscribe","symbol":"%s"}' % symbol
            log.info('Successfully opened a connection!')
            ws.send(command)

    def run(self):
        self.ws.run_forever()

if __name__ == "__main__":
    FINNHUB_API_KEY = config.finnhub_api_key
    client = FinnhubWebsocketClient(FINNHUB_API_KEY)
    client.run()
