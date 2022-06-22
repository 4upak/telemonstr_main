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
from threading import Thread

@app.task
def streamer_controller():

    bundles = BinanceBudle.objects.all()
    pairs = []
    pair_ids = []
    for bundle in bundles:
        if bundle.first_pair.pk not in pair_ids:
            pairs.append({'symbol': bundle.first_pair.symbol, 'pk': bundle.first_pair.pk})
            pair_ids.append(bundle.first_pair.pk)

        if bundle.second_pair.pk not in pair_ids:
            pairs.append({'symbol':bundle.second_pair.symbol, 'pk':bundle.second_pair.pk})
            pair_ids.append(bundle.second_pair.pk)

        if bundle.third_pair.pk not in pair_ids:
            pairs.append({'symbol':bundle.third_pair.symbol, 'pk':bundle.third_pair.pk})
            pair_ids.append(bundle.third_pair.pk)


    threads = []
    for pair in pairs:
        t = Thread(target=start_socket, args=(pair,))
        threads.append(t)
        t.start()