import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def get_account_info(account):
    try:
        f = open(f"accounts/sessions/import/{account}.json", "r")
        with f as read_file:
            return json.load(read_file)
    except Exception as ex:
        return False

def get_free_proxy():
    from .models import Telegram_account
    from .models import Proxy

    online_proxy_list = Telegram_account.objects.filter(online=1).values('proxy_id').all()
    online_proxy_ids = []

    for online_proxy in online_proxy_list:
        online_proxy_ids.append(int(online_proxy.get('proxy_id')))
    inactive_proxy = Proxy.objects.exclude(pk__in=online_proxy_ids).first()

    return inactive_proxy

def ws_log(type, channel_name, data):
    try:
        channel_layer = get_channel_layer()
        if type == 'account.action':
            async_to_sync(channel_layer.group_send)(
                str(channel_name),
                {
                    'type': type,
                    'text': json.dumps(data)
                }
            )
        if type == 'account.message':
            async_to_sync(channel_layer.group_send)(
                str(channel_name),
                {
                    'type': type,
                    'text': str(data)
                }
            )

        return True
    except Exception as ex:
        return False

