from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from .telethon_functions import account_controller

from .tasks import start_account_controller

class AccountsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.account_id = self.scope['url_route']['kwargs']['account_id']
        print(self.account_id)
        print(self.channel_name)
        await self.channel_layer.group_add(self.account_id, self.channel_name)
        start_account_controller.delay(self.account_id)

        await self.accept()




    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.account_id, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):

        json_data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.account_id,
            {
                'type': 'account.message',
                'text': json_data['message']
            }
        )

    async def account_message(self, event):
        await self.send(text_data = event['text'])

