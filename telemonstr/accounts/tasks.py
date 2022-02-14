import requests

from .models import Telegram_account
import time

def start_account_controller():
    for i in range(0,100):
        print(i)
        time.sleep(5)