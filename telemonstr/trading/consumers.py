from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from trading.models import BinancePair
from .models import Bundle
from .tasks import *

class TradingConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add('dashboard', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('dashboard', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        #json_data = json.loads(text_data)
        json_data = {}
        json_data['message'] = "Привет"
        await self.channel_layer.group_send(
            'dashboard',
            {
                'type': 'trading.message',
                'text': json_data['message']
            }
        )

    async def trading_message(self, event):
        data = {
            'type': 'message',
            'value': event['text']
        }
        await self.send(text_data=json.dumps(data))

    async def trading_action(self, event):
        await self.send(text_data = event['text'])



class StreamingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.symbol = self.scope['url_route']['kwargs']['symbol']
        await self.channel_layer.group_add(self.symbol, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.symbol, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        #json_data = json.loads(text_data)
        json_data = {}
        json_data['message'] = "Hello"
        await self.channel_layer.group_send(
            self.symbol,
            {
                'type': 'streaming.message',
                'text': json_data['message']
            }
        )

    async def streaming_message(self, event):
        data = {
            'type': 'message',
            'value': event['text']
        }
        await self.send(text_data=json.dumps(data))

    async def streaming_action(self, event):
        await self.send(text_data = event['text'])
