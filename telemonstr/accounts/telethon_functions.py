import asyncio
from channels.layers import get_channel_layer


async def account_controller(account_id, counsumer):
    print('async controller 1')
    channel_layer = get_channel_layer()
    print('async controller 2')
    for i in range(10):
        print('async controller 3')
        await channel_layer.group_send(
            account_id,
            {
                'type': 'account.message',
                'text': f'{i} Account is online in commands'
            }

        )
        await asyncio.sleep(10)