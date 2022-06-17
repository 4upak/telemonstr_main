import requests
from bs4 import BeautifulSoup
import lxml
import json
from requests.structures import CaseInsensitiveDict

def bestchange_count_stock_glass(data):

    total_crypto = 0
    total_fiat = 0
    for item in data:
        total_crypto = total_crypto + float(item['total'])
        total_fiat = total_fiat + float(item['price']) * float(item['total'])
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


def count_fiat_bestchange(crypto_label,fiat_label,type,payment_method):
    if crypto_label == 'usdt':
        crypto_label = 'tether-trc20'
    if payment_method == 'privatbank':
        payment_method = 'privat24-uah'

    if type== 'buy':
        url = f"https://www.bestchange.ru/{crypto_label}-to-{payment_method}.html"
    if type == 'sell':
        url = f"https://www.bestchange.ru/{payment_method}-to-{crypto_label}.html"


    bestchange_answer = requests.get(url).text

    soup = BeautifulSoup(bestchange_answer, 'lxml')
    name_items = soup.select("#content_table > tbody > tr > td.bj > div > div > div")

    if type== 'buy':
        price_items = soup.select("#content_table > tbody > tr > td:nth-child(4)")
    if type == 'sell':
        price_items = soup.select("#content_table > tbody > tr > td > div.fs")


    reserv_items = soup.select("#content_table > tbody > tr > td.ar.arp")

    data = []
    i=0
    for name in name_items:
        price = float(price_items[i].text.split(' ')[0])
        total = float(reserv_items[i].text.replace(" ",""))/price
        data.append(
            {
                'name':name.text,
                'price':price,
                'total': total
            }
        )
        i+=1
    print(data)
    result = {
        'stock': 'bestchange',
        'crypto': crypto_label,
        'fiat': fiat_label,
        'type': type,
        'bank': payment_method,
        'avg': bestchange_count_stock_glass(data[:10]),
        'optimal': bestchange_count_stock_glass(data[6:10]),
        'top5': bestchange_count_stock_glass(data[:5])
    }


    return result