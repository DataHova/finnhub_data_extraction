import websocket
from websocket._app import WebSocketApp
from websocket._logging import enableTrace


def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    enableTrace(True)
    ws = WebSocketApp("wss://ws.finnhub.io?token=ckvnf59r01qq199j31egckvnf59r01qq199j31f0",
                      on_message = on_message,
                      on_error = on_error,
                      on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
