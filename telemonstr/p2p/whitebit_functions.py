import json
import requests

def count_fiat_whitebit(crypto, fiat, type):
    crypto = crypto.upper()
    fiat = fiat.upper()
    url = f"https://whitebit.com/api/v2/public/depth/{crypto}_{fiat}"
    whitebit_answer = requests.get(url).text
    data = json.loads(whitebit_answer)
    ask = data['result']['asks'][0][0]
    bid = data['result']['bids'][0][0]

    if type=='sell':
        price = float(ask)

    elif type=='buy':
        price = float(bid)

    else:
        price = 0
    result = {
        'stock': 'whitebit',
        'crypto': crypto,
        'fiat': fiat,
        'type': type,
        'bank': 'stock',
        'avg': price,
        'optimal': {'avg_price': price},
        'top5': {'avg_price': price}
    }
    return result