from telemonstr.celery import app
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

@app.task
def start_account_controller(account_id):
    channel_layer = get_channel_layer()
    for i in range(10):
        print(f'iteractio {i} for {account_id} account_id')
        async_to_sync(channel_layer.group_send)(
            '1',
            {
                'type': 'account.message',
                'text': f'iteractio {i} for {account_id} account_id'
            }

        )
        time.sleep(10)
    return json.dumps({'status': 'ok'})