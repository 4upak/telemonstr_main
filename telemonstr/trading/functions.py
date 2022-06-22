import requests
import json
import datetime
from binance.client import Client
import binance
from binance import exceptions
import math
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import *
import time
import websocket
from .tasks import *
from django.db.models import Q
from random import randrange
from functools import partial

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)



def price(symbol):
    price = client.get_avg_price(symbol=symbol)['price']
    return float(price)


def balance(symbol):
    balance = client.get_asset_balance(asset=symbol, recvWindow=50000)
    return balance


def order_market_buy(symbol, quantity):
    client.order_market_buy(symbol=symbol, quantity=quantity, recvWindow=50000)


def order_market_sell(symbol, quantity):
    client.order_market_sell(symbol=symbol, quantity=quantity, recvWindow=50000)


def check(name_1, name_2):
    try:
        symbol = name_2 + name_1
        order_market_sell(symbol, float(balance(name_2)['free']))
        print('check')
    except Exception as e:
        print('нет check', e)


def get_symbol_info(n1, n2):
    try:
        one = client.get_symbol_info(n1 + n2)
        q = float(one['filters'][2]['stepSize'])
        precision = int(round(-math.log(q, 10), 0))
        return precision
    except Exception as e:
        pass
        # print('Нет get_symbol_info', e)


def ws_log(type, channel_name, data):
    try:
        channel_layer = get_channel_layer()
        if type == 'trading.action':
            async_to_sync(channel_layer.group_send)(
                str(channel_name),
                {
                    'type': type,
                    'text': json.dumps(data)
                }
            )
        if type == 'trading.message':
            async_to_sync(channel_layer.group_send)(
                str(channel_name),
                {
                    'type': type,
                    'text': str(data)
                }
            )
        if type == 'streaming.message':
            async_to_sync(channel_layer.group_send)(
                str(channel_name),
                {
                    'type': type,
                    'text': str(data)
                }
            )
        return True
    except Exception as ex:
        return False


def binance_torg():
    try:
        bookTicker = requests.get('https://api.binance.com/api/v3/ticker/bookTicker')
        bookTicker = json.loads(bookTicker.text)
        Book = {}
        for block in bookTicker:
            Book.update({block["symbol"]: [block["bidPrice"], block["askPrice"]]})

        Info_list = requests.get('https://api.binance.com/api/v3/exchangeInfo')
        Info_list = json.loads(Info_list.text)

        Data = {}
        lis = []
        for block in Info_list["symbols"]:
            if block["status"] == "TRADING" and 'UP' not in block['symbol'] and 'DOWN' not in block['symbol']:
                Data.update({block["baseAsset"]: {}})
                Data.update({block["quoteAsset"]: {}})

        for block in Info_list["symbols"]:
            if block["status"] == "TRADING" and 'UP' not in block['symbol'] and 'DOWN' not in block['symbol']:
                Data[block["baseAsset"]].update({block["quoteAsset"]: float(Book[block["symbol"]][0])})
                Data[block["quoteAsset"]].update({block["baseAsset"]: 1 / (float(Book[block["symbol"]][1]))})

        for one_name in Data:
            for two_name in Data[one_name]:
                for tree_name in Data[two_name]:
                    for four_name in Data[tree_name]:
                        if four_name == one_name:
                            sum_start = 1
                            tr_1 = Data[one_name][two_name] * sum_start
                            tr_2 = Data[two_name][tree_name] * tr_1
                            sum_end = Data[tree_name][four_name] * tr_2
                            pro = (sum_end - sum_start) / sum_end * 100
                            exclude_list = ['BIDR']
                            if pro not in lis and one_name not in exclude_list and two_name not in exclude_list and tree_name not in exclude_list:
                                now = datetime.datetime.now()

                                data = {
                                    'action': 'new_funnel',
                                    'one_name': one_name,
                                    'two_name': two_name,
                                    'tree_name':tree_name,
                                    'four_name':four_name,
                                    'pro':pro,
                                    'time':now.strftime("%H:%M:%S")
                                }
                                if (Bundle.objects.filter(start_symbol=one_name).filter(one_step=two_name).filter(two_step=tree_name).filter(final_step=four_name).count()==0):
                                    b = Bundle(
                                        start_symbol  = one_name,
                                        one_step = two_name,
                                        two_step = tree_name,
                                        final_step = four_name,
                                        profitability = float(pro)
                                    )
                                    print(f"Bundle {b.start_symbol}->{b.one_step}->{b.two_step}->{b.final_step} created. Profitability = {b.profitability}")
                                else:
                                    b = Bundle.objects.filter(start_symbol=one_name).filter(one_step=two_name).filter(two_step=tree_name).filter(final_step=four_name).first()
                                    b.profitability = float(pro)
                                    print(f"Bundle {b.start_symbol}->{b.one_step}->{b.two_step}->{b.final_step} updated. Profitability = {b.profitability}")
                                b.save()

                                ws_log('trading.action', 'dashboard', json.dumps(data))


    except Exception as ex:
        print(ex)
        return 0

def start_socket(pair):
    def on_message(ws, message, pk):
        data = json.loads(message)
        if data['s'] == 'ETHUSDT':
            if randrange(1,10) == 5:
                ws_log('streaming.message', 'all', {'symbol':data['s'], 'price':data['p'], 'pk':pk})
        elif data['s'] == 'BTCUSDT':
            if randrange(1,10) == 5:
                ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})

        elif data['s'] == 'BTCBUSD':
            if randrange(1,10)%3 == 0:
                ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})

        elif data['s'] == 'ETHBUSD':
            if randrange(1,10)%2 == 0:
                ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})

        elif data['s'] == 'BUSDUSDT':
            if randrange(1,10)%2 == 0:
                ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})

        elif data['s'] == 'USDCUSDT':
            if randrange(1,10)%2 == 0:
                ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})

        elif data['s'] == 'BNBUSDT':
            if randrange(1,10)%2 == 0:
                ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})

        elif data['s'] == 'ETHBTC':
            if randrange(1,10)%2 == 0:
                ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})

        elif data['s'] == 'ADAUSDT':
            if randrange(1,10)%2 == 0:
                ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})

        else:
            ws_log('streaming.message', 'all', {'symbol': data['s'], 'price': data['p'], 'pk':pk})





    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        print("### connected ###")

    ws = websocket.WebSocketApp(f"wss://stream.binance.com:9443/ws/{pair['symbol'].lower()}@aggTrade",
                                on_message=partial(on_message, pk=pair['pk']),
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


def start_sockets():
    from threading import Thread

    pairs = BinancePair.objects.all()
    bundles = BinanceBudle.objects.all()
    pairs = []
    for bundle in bundles:
        pairs.append(bundle.first_pair.symbol)
        pairs.append(bundle.second_pair.symbol)
        pairs.append(bundle.third_pair.symbol)
    pairs = list(set(pairs))

    threads = []
    for pair in pairs:
        t = Thread(target=start_socket, args=(pair,))
        threads.append(t)
        t.start()

def build_binance_bundles(start):
    bundles = []
    pairs = BinancePair.objects.all()

    next = ''
    next_next = ''
    next_next_next = ''
    first_step_pairs = BinancePair.objects.filter(Q(base_asset = start) | Q(second_asset = start))
    data = []
    for first_step_pair in first_step_pairs:
        if first_step_pair.base_asset == start:
            next = first_step_pair.second_asset
        if first_step_pair.second_asset == start:
            next = first_step_pair.base_asset

        second_step_pairs = BinancePair.objects.filter(Q(base_asset = next) | Q(second_asset = next))
        for second_step_pair in second_step_pairs:
            if second_step_pair.base_asset == next:
                next_next = second_step_pair.second_asset
            if second_step_pair.second_asset == next:
                next_next = second_step_pair.base_asset
            if next_next != start:
                third_step_pairs = BinancePair.objects.filter(Q(base_asset=next_next) | Q(second_asset=next_next))
                for third_step_pair in third_step_pairs:
                    if third_step_pair.base_asset == next_next:
                        next_next_next = third_step_pair.second_asset
                    if third_step_pair.second_asset == next_next:
                        next_next_next = third_step_pair.base_asset

                    #print(f"{start} -> {next} -> {next_next} -> {next_next_next}")
                    if start == next_next_next:
                        bundle = BinanceBudle(
                            start_stop_symbol = start,
                            first_step_symbol = next,
                            first_pair = first_step_pair,
                            second_step_symbol = next_next,
                            second_pair = second_step_pair,
                            third_pair = third_step_pair,
                        )
                        bundle.save()





    '''second_step_pairs = BinancePair.objects.filter(Q(base_asset=next) | Q(second_asset=next))
    for second_step_pair in second_step_pairs:
        if second_step_pair.base_asset == start:
            final = second_step_pair.second_asset
        if second_step_pair.second_asset == start:
            final = second_step_pair.base_asset'''


    '''for bundle in bundles:
        print(f"{bundle['first']} -> {bundle['second']} -> {bundle['third']}")'''

def channge_assets():
    f = open('trading/bundles.txt', 'r')
    lines = f.readlines()
    for symbol in lines:
        symbol = symbol.replace('\n','')
        pair = BinancePair.objects.filter(symbol=symbol).first()
        buf = pair.base_asset
        pair.base_asset = pair.second_asset
        pair.second_asset = buf
        pair.save()


    f.close()