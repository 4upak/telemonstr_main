import asyncio
from channels.layers import get_channel_layer
from .functions import *
from telethon import TelegramClient, sync
from telethon import events
from telethon import functions, types
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerUser, PeerChat, PeerChannel, User, Channel, Chat
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from asgiref.sync import async_to_sync
import socks


def get_client(account):
    channel_layer = get_channel_layer()
    proxy = get_free_proxy()

    if proxy.port == 45786:
        proxy.port = 45785
    try:

        session_url = f"accounts/sessions/active/{account.session_file}.session"
        print(session_url)

        client = TelegramClient(session_url, api_id=14149, api_hash='89b7a2dd87e472556eab6757cf6d36ce')
        client.connect()
    except Exception as ex:
        async_to_sync(channel_layer.group_send)(
            str(account.id),
            {
                'type': 'account.message',
                'text': str(ex)
            }

        )
        return False

    else:
        async_to_sync(channel_layer.group_send)(
            str(account.id),
            {
                'type': 'account.message',
                'text': 'client conected'
            }

        )
        return client


async def main_controller(client, me, account):
    client.start()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(account.id),
        {
            'type': 'account.message',
            'text': 'Main controller started'
        }

    )


    iteration_number = 0
    while True:

        iteration_number +=1
        async_to_sync(channel_layer.group_send)(
            str(account.id),
            {
                'type': 'account.message',
                'text': f'iteration number: {iteration_number}'
            }
        )
        if iteration_number>10:
            break




async def main_handle(client, account):
    channel_layer = get_channel_layer()
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        sender = await event.get_sender()
        data = {
            'sender':sender.id,
            'me':me.id,
            'telegram_message':event.raw_text
        }
        channel_layer.group_send(
            str(account.id),
            {
                'type': 'account.json',
                'text': json.dumps(data)
            }
        )

    client.start()
    me = await client.get_me()

    account.telegram_user_id = me.id
    account.save()

    data = {
        'action': 'change_telegram_user_id',
        'account_id': account.id,
        'telegram_user_id': me.id
    }

    channel_layer.group_send(
        str(account.id),
        {
            'type': 'account.message',
            'text': f'Main handle started, telegram_user_id:{me.id}'
        }
    )
    await main_controller(client, me, account)




