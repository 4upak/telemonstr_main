import requests
import json
from requests.structures import CaseInsensitiveDict

def get_huobi_bank_id(bank):
    url = "https://otc-api.trygofast.com/v1/data/config-list?type=currency,marketQuery,pay,allCountry"

    resp = requests.get(url).json()
    result = 0
    for item in resp['data']['payMethod']:

        if item['name'].replace(" ", "").lower() == bank.replace(" ", "").lower():
            result = int(item['payMethodId'])
    return result

def get_huobi_currency_id(fiat_label):
    url = "https://otc-api.trygofast.com/v1/data/config-list?type=currency,marketQuery,pay,allCountry"

    resp = requests.get(url).json()
    result = 0
    for item in resp['data']['currency']:
        if item["nameShort"].replace(" ", "").lower() == fiat_label.replace(" ", "").lower():
            result = int(item["currencyId"])
    return result

def get_huobi_crypto_id(crypto_label):
    url = "https://otc-api.trygofast.com/v1/data/config-list?type=currency,marketQuery,pay,allCountry"

    resp = requests.get(url).json()
    result = 0
    for item in resp['data']['marketQuery']:
        if item["coinName"].replace(" ", "").lower() == crypto_label.replace(" ", "").lower():
            result = int(item["coinId"])
    return result

def huobi_count_stock_glass(data):

    total_crypto = 0
    total_fiat = 0
    for item in data:
        total_crypto = total_crypto + float(item['tradeCount'])
        total_fiat = total_fiat + float(item['price']) * float(item['tradeCount'])
    if total_fiat != 0 and total_crypto != 0:
        avg_price = total_fiat / total_crypto
    else:
        avg_price = 0
    result = {
        'total_crypto': round(total_crypto, 2),
        'total_fiat': round(total_fiat, 2),
        'avg_price': round(avg_price, 2),
    }
    return result


def count_fiat_huobi(crypto_label,fiat_label,type,payment_method):
    bank_id = get_huobi_bank_id(payment_method)
    currency_id = get_huobi_currency_id(fiat_label)
    crypto_id = get_huobi_crypto_id(crypto_label)

    if type == "buy":
        url = f"https://otc-api.trygofast.com/v1/data/trade-market?coinId={crypto_id}&currency={currency_id}&tradeType=sell&currPage=1&payMethod={bank_id}&acceptOrder=-1&country=&blockType=general&online=1&range=0&amount=&onlyTradable=false"

    if type == "sell":
        url = f"https://otc-api.trygofast.com/v1/data/trade-market?coinId={crypto_id}&currency={currency_id}&tradeType=buy&currPage=1&payMethod={bank_id}&acceptOrder=-1&country=&blockType=general&online=1&range=0&amount=&onlyTradable=false"

    print(url)
    bybit_answer = requests.get(url).json()


    result = {
        'stock': 'huobi',
        'crypto': crypto_label,
        'fiat': fiat_label,
        'type': type,
        'bank': payment_method,
        'avg': huobi_count_stock_glass(bybit_answer['data']),
        'optimal': huobi_count_stock_glass(bybit_answer['data'][:5]),
        'top5': huobi_count_stock_glass(bybit_answer['data'][:5])
    }

    return result