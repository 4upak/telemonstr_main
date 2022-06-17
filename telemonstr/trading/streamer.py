import websocket





def streamer(symbol):
    def on_message(ws, message):
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        print("### connected ###")
    ws = websocket.WebSocketApp(f"wss://stream.binance.com:9443/ws/{symbol}@aggTrade",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()