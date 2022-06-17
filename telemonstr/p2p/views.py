from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import requests
import time
from bs4 import BeautifulSoup
import json
from .functions import *
from .huobi_functions import *
from .bestchange_functions import *
import time

def binance_dashboard(request,fiat, crypto, bank):
    result = []
    result.append(exchange_get_dashboard_data(fiat, crypto, bank, 'binance'))
    #result.append(exchange_get_dashboard_data(fiat, crypto, bank, 'bybit'))
    result.append(exchange_get_dashboard_data(fiat, crypto, bank, 'huobi'))
    result.append(exchange_get_dashboard_data(fiat, crypto, bank, 'bestchange'))



    data = {'title': "Дашборд",'fiat':fiat,'crypto':crypto, 'data': result}

    return render(request, 'p2p.html', context=data)
    #return HttpResponse(json.dumps(result), content_type="application/json")

def binance_get_currency_list(request, fiat):
    result = get_buy_area(fiat)
    return HttpResponse(json.dumps(result), content_type="application/json")

def binance_bank_list(request, fiat):
    result = get_bank_list(fiat)
    return HttpResponse(json.dumps(result), content_type="application/json")

def test_page(request,crypto_label,fiat_label,type,payment_method):

    result = count_fiat(crypto_label,fiat_label,type,payment_method)

    return HttpResponse(json.dumps(result), content_type="application/json")

def bybit_dashboard(request,crypto, fiat, bank):
    result = count_fiat_bybit(crypto,fiat,"sell",bank)
    #result = get_bybit_banks()
    return HttpResponse(json.dumps(result), content_type="application/json")

def huobi_dashboard(request,crypto, fiat, bank):
    result = count_fiat_huobi(crypto, fiat, "buy", bank)
    return HttpResponse(json.dumps(result), content_type="application/json")

def bestchange_dashboard(request,crypto, fiat, bank):
    result = count_fiat_bestchange(crypto, fiat, 'sell', bank)
    return HttpResponse(json.dumps(result), content_type="application/json")