from telemonstr.celery import app
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from .models import Telegram_account
from .telethon_functions import main_handle
from .functions import *

@app.task
def start_account_controller(account_id):
    channel_layer = get_channel_layer()
    from .telethon_functions import get_client
    account = Telegram_account.objects.get(pk=account_id)
    data = {
        'action': 'message',
        'account_id': account.id,
        'telegram_user_id': '-'
    }
    ws_log('account.action', account.id, data)
    client = get_client(account)

    with client:
        client.loop.run_until_complete(main_handle(client,account))
        data = {
            'action': 'account_stopped',
            'account_id': account.id,
        }

        ws_log('account.action', account.id, data)

