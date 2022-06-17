from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json

from .tasks import start_account_controller

class AccountsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.account_id = self.scope['url_route']['kwargs']['account_id']
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

        await self.channel_layer.group_send(
            self.account_id,
            {
                'type': 'account.action',
                'text': json_data['message']
            }
        )

        await self.channel_layer.group_send(
            self.account_id,
            {
                'type': 'account.json',
                'text': json_data['message']
            }
        )

    async def account_message(self, event):
        data = {
            'type':'message',
            'value': event['text']
        }
        await self.send(text_data = json.dumps(data))

    async def account_action(self, event):
        data = {
            'type': 'action',
            'value': event['text']
        }
        await self.send(text_data = json.dumps(data))

    async def account_json(self, event):
        data = {
            'type': 'action',
            'value': event['text']
        }
        await self.send(text_data = json.dumps(data))