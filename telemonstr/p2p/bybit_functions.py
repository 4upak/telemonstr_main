import requests
import json
from requests.structures import CaseInsensitiveDict

def get_bybit_bank_id(bank):
    url = "https://api2.bybit.com/spot/api/v1/otc/payment/broker_config_list"

    headers = CaseInsensitiveDict()
    headers["authority"] = "api2.bybit.com"
    headers["accept"] = "application/json"
    headers["accept-language"] = "ru-RU"
    headers["Content-Length"] = "0"
    headers["content-type"] = "application/x-www-form-urlencoded"
    headers["guid"] = "f8ec7106-2f01-7d15-38da-6f14c4b3108e"

    resp = requests.post(url, headers=headers).json()
    result = 0
    for item in resp['result']:
        if item['paymentName'].replace(" ","").lower() == bank.replace(" ","").lower():
            result = int(item['paymentType'])
    return result

def bybit_count_stock_glass(data):

    total_crypto = 0
    total_fiat = 0
    for item in data:
        total_crypto = total_crypto + float(item['lastQuantity'])
        total_fiat = total_fiat + float(item['price']) * float(item['lastQuantity'])
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


def count_fiat_bybit(crypto_label,fiat_label,type,payment_method):
    bank_id = get_bybit_bank_id(payment_method)
    if type == "sell":
        type_id = 0
    if type == "buy":
        type_id = 1
    url = "https://api2.bybit.com/spot/api/otc/item/list"

    headers = CaseInsensitiveDict()
    headers["authority"] = "api2.bybit.com"
    headers["content-type"] = "application/x-www-form-urlencoded"
    headers["accept"] = "application/json"
    headers["guid"] = "f89defd2-a0ec-5641-dbb9-7309a7e4dce1"

    data = f"tokenId={crypto_label.upper()}&currencyId={fiat_label.upper()}&payment={bank_id}&side={type_id}&size=10&page=1&amount="
    bybit_answer = requests.post(url, headers=headers, data=data).json()


    result = {
        'stock': 'bybit',
        'crypto': crypto_label,
        'fiat': fiat_label,
        'type': type,
        'bank': payment_method,
        'avg': bybit_count_stock_glass(bybit_answer['result']['items']),
        'optimal': bybit_count_stock_glass(bybit_answer['result']['items'][6:]),
        'top5': bybit_count_stock_glass(bybit_answer['result']['items'][:5])
    }

    return result