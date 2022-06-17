from telemonstr.celery import app
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
import binance
from binance.client import Client
import json
import datetime
import binance
from binance import exceptions
import binance
from binance import exceptions
import math
import time
import datetime
from django.utils import timezone
from .functions import *
from .models import *

def streamer(symbol):
    def on_message(ws, message):
        pair = BinancePair.objects.filter(symbol = message['s']).first()
        pair.last_price = message['p']
        pair.save()

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

def update_binace_pairs():
    from .models import BinancePair
    with open('data.txt') as f:
        lines = f.readlines()
        i=0
        for line in lines:
            pair = BinancePair(
                symbol = line.replace('/','').rstrip(),
                base_asset = line.split('/')[0].rstrip(),
                second_asset = line.split('/')[1].rstrip()
            )
            try:
                pair.save()
            except Exception as ex:
                print(ex)
            i+=1
    return i

@app.task
def clear_bundles():
    while True:
        delta_time = timezone.now() - datetime.timedelta(seconds=600)
        count = Bundle.objects.filter(date__lt=delta_time).count()
        if count>0:
            Bundle.objects.filter(date__lt=delta_time).delete()
        print(f"Old {count} bundles deleted")
        time.sleep(600)
    ws_log('trading.message', 'dashboard', 'Old bundles cleared')

@app.task
def start_trading_controller():
    ws_log('trading.message', 'dashboard', f'task started')
    while True:
        binance_torg()
        time.sleep(1)
    ws_log('trading.message', 'dashboard', 'task terminated')

@app.task
def test_controller():
    while True:
        print('work')
        time.sleep(3)

@app.task
def streamer_controller(symbol):
    def on_message(ws, message):
        data = json.loads(message)
        print(data)
        pair = BinancePair.objects.filter(symbol=data['s']).first()
        pair.last_price = float(data['p'])
        pair.save()



    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        print("### connected ###")

    ws = websocket.WebSocketApp(f"wss://stream.binance.com:9443/ws/{symbol.lower()}@aggTrade",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
