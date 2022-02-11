import time
import asyncio
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):


    def handle(self, *args, **options):
        channel_layer = get_channel_layer()
        for i in range(10):
            print(f'{i} Account is online in commands')
            async_to_sync(channel_layer.group_send)(
                '1',
                {
                    'type': 'account.message',
                    'text': f'{i} Account is online in commands'
                }

            )
            time.sleep(10)