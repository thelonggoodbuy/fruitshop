from config.celery import app
from celery import shared_task
import logging
import random

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from django.core.cache import cache


@shared_task
def task_buy_pineapple():
    print("You want pineapple")
    print('-----CURRENT----CACHE------')
    pineapple_data = cache.get('pineapple_key')
    # print(cache.get('pineapple_key'))
    print(pineapple_data)
    print('---------------------------')


    if pineapple_data:
        pineapple_quantity = int(pineapple_data)
        cache.delete('pineapple_key')
    else:
        pineapple_quantity = random.randint(10, 20)


    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
                'type': 'chat_message',
                'message': f'Do you want to buy {pineapple_quantity} pineapple?',
                "KEY_PREFIX": "fruit_shop",
        }
    )





@shared_task
def task_two():
    print("This is task two")
