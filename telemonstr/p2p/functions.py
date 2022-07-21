import requests
import json
from requests.structures import CaseInsensitiveDict
from .huobi_functions import *
from .bybit_functions import *
from .bestchange_functions import *
from .minfin_functions import *
from .whitebit_functions import *


def count_stock_glas(data):
    total_crypto = 0
    total_fiat = 0
    for item in data:
        total_crypto = total_crypto + float(item['adv']['tradableQuantity'])
        total_fiat = total_fiat + float(item['adv']['price']) * float(item['adv']['tradableQuantity'])
    if total_fiat!= 0 and total_crypto!=0:
        avg_price = total_fiat / total_crypto
    else:
        avg_price = 0
    result = {
        'total_crypto': round(total_crypto,2),
        'total_fiat': round(total_fiat,2),
        'avg_price': round(avg_price,2),
    }
    return result

def get_buy_area(fiat):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/portal/config"
    headers = {
        "Host": "p2p.binance.com",
        "Content-Type": "application/json",
        "Bnc-Uuid": "2499f661-d090-4120-913f-b2437ec0b789",
    }
    payload = {
        "fiat": fiat,
    }
    binance_answer = requests.post(url, data=json.dumps(payload), headers=headers).json()
    buy_assets = binance_answer['data']['areas'][0]['tradeSides'][0]['assets']
    sell_assets = binance_answer['data']['areas'][0]['tradeSides'][1]['assets']
    result = {
        'buy': buy_assets,
        'sell': sell_assets,
    }
    return result

def count_fiat(crypto_label,fiat_label,type,payment_method):
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    headers = {
        "Host": "p2p.binance.com",
        "Content-Type": "application/json",
        "Bnc-Uuid": "2499f661-d090-4120-913f-b2437ec0b789",
    }
    payload = {
        "page": 1,
        "rows": 10,
        "payTypes": [payment_method],
        "asset": crypto_label,
        "tradeType": type,
        "fiat": fiat_label
    }
    # Adding empty header as parameters are being sent in payload
    binance_answer = requests.post(url, data=json.dumps(payload), headers=headers).json()

    result = {
        'stock': 'binance',
        'crypto':crypto_label,
        'fiat':fiat_label,
        'type':type,
        'bank':payment_method,
        'avg': count_stock_glas(binance_answer['data']),
        'optimal': count_stock_glas(binance_answer['data'][6:]),
        'top5': count_stock_glas(binance_answer['data'][:5])
    }

    return result

def get_bank_list(fiat):
    url = "https://p2p.binance.com/bapi/c2c/v2/public/c2c/adv/filter-conditions"
    headers = {
        "Host": "p2p.binance.com",
        "Content-Type": "application/json",
        "Bnc-Uuid": "2499f661-d090-4120-913f-b2437ec0b789",
    }

    payload = {
        "fiat": fiat
    }
    binance_answer = requests.post(url, data=json.dumps(payload), headers=headers).json()
    result = []
    for item in binance_answer['data']['tradeMethods']:
        result.append(item['identifier'])
    return result




def exchange_get_dashboard_data(fiat, crypto, bank, stock):

    result = []
    if stock == "binance":
        buy_data = count_fiat(crypto, fiat, 'buy', bank)
        sell_data = count_fiat(crypto, fiat, 'sell', bank)

    '''if stock == "bybit":
        buy_data = count_fiat_bybit(crypto, fiat, 'buy', bank)
        sell_data = count_fiat_bybit(crypto, fiat, 'sell', bank)'''

    if stock == "huobi":
        buy_data = count_fiat_huobi(crypto, fiat, 'buy', bank)
        sell_data = count_fiat_huobi(crypto, fiat, 'sell', bank)

    '''if stock == "bestchange":
        buy_data = count_fiat_bestchange(crypto, fiat, 'buy', bank)
        sell_data = count_fiat_bestchange(crypto, fiat, 'sell', bank)'''

    if stock == "minfin":
        buy_data = count_fiat_minfin_new('buy')
        sell_data = count_fiat_minfin_new('sell')

    if stock == "whitebit":
        buy_data = count_fiat_whitebit(crypto, fiat, 'buy')
        sell_data = count_fiat_whitebit(crypto, fiat, 'sell')


    spread = round(buy_data['optimal']['avg_price'] - sell_data['optimal']['avg_price'], 2)
    spread_top5 = round(buy_data['top5']['avg_price'] - sell_data['top5']['avg_price'], 2)

    if buy_data['optimal']['avg_price'] != 0:
        spread_percent_buy = round(spread / buy_data['optimal']['avg_price'] * 100, 2)
    else:
        spread_percent_buy = 0

    if sell_data['optimal']['avg_price'] != 0:
        spread_percent_sell = round(spread / sell_data['optimal']['avg_price'] * 100, 2)
    else:
        spread_percent_sell = 0

    buy_data['spread'] = spread
    buy_data['spread_top5'] = spread_top5
    buy_data['spread_percent'] = spread_percent_buy
    sell_data['spread'] = spread
    sell_data['spread_top5'] = spread_top5
    sell_data['spread_percent'] = spread_percent_sell

    result.append(buy_data)
    result.append(sell_data)

    return result



