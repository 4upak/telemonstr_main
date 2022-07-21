import requests
from bs4 import BeautifulSoup
import lxml
import json
from requests.structures import CaseInsensitiveDict

def bestchange_count_stock_glass(data):
    pass




def count_fiat_minfin(type):

    url = "https://minfin.com.ua/ua/currency/auction/"
    bestchange_answer = requests.get(url).text
    soup = BeautifulSoup(bestchange_answer, 'lxml')
    if type == "buy":
        reserv_items = soup.select("#exchanges-page-container > div > div > div.exchanges-page-header > div > div.chart-button-wrapper > div > div.chart-wrapper > div > div.buy > span.Typography")
    if type == "sell":
        reserv_items = soup.select("#exchanges-page-container > div > div > div.exchanges-page-header > div > div.chart-button-wrapper > div > div.chart-wrapper > div > div.sale > span.Typography")


    price = float(reserv_items[0].next_element.replace(',','.'))
    result = {
        'stock': 'minfin',
        'crypto': 'usdt',
        'fiat': 'uah',
        'type': type,
        'bank': 'cash',
        'avg': price,
        'optimal': {'avg_price':price},
        'top5': {'avg_price':price}
    }
    return result

def count_fiat_minfin_new(type):
    url = "https://minfin.com.ua/ua/currency/auction/exchanger/kiev/id-615434906f6000562f8e4b96/"
    bestchange_answer = requests.get(url).text
    soup = BeautifulSoup(bestchange_answer, 'lxml')
    if type == "buy":
        reserv_items = soup.select(
            "#rateNav > tbody > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1)")
    if type == "sell":
        reserv_items = soup.select(
            "#rateNav > tbody > tr:nth-child(1) > td:nth-child(3) > div:nth-child(1)")

    price = float(reserv_items[0].next_element.replace(',', '.'))
    result = {
        'stock': 'minfin',
        'crypto': 'usdt',
        'fiat': 'uah',
        'type': type,
        'bank': 'cash',
        'avg': price,
        'optimal': {'avg_price': price},
        'top5': {'avg_price': price}
    }
    return result
