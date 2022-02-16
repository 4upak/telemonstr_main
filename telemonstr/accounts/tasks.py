from telemonstr.celery import app
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

@app.task
def start_account_controller(account_id):
    channel_layer = get_channel_layer()

    for i in range(3):
        async_to_sync(channel_layer.group_send)(
            account_id,
            {
                'type': 'account.message',
                'text': f'iteractio {i} for {account_id} account_id'
            }

        )
        time.sleep(10)
    return json.dumps({'status': 'ok', 'account_id':account_id})