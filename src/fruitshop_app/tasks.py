from config.celery import app
from celery import shared_task
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache

from django.apps import apps









@shared_task
def task_buy_pineapple():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    pineapple_data = cache.get('pineapple_key')

    if pineapple_data:
        pineapple_quantity = int(pineapple_data)
        cache.delete('pineapple_key')
    else:        
        pineapple_quantity = random.randint(1, 10)

    pineapple_buy_cost = 3
    pineapple_cost = pineapple_buy_cost*pineapple_quantity
    pineapple_obj = Commodity.objects.get(raw_title='pineapple')
    pineapple_obj.quantity += pineapple_quantity
    pineapple_obj.save()
    account_obj = Account.objects.first()
    account_obj.total_debt -= pineapple_cost
    account_obj.save()

    message = {'change_store': {'pineapple': pineapple_obj.quantity},
                    'change_account': str(account_obj.total_debt)}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'chat_message',
            'message': message,
            "KEY_PREFIX": "fruit_shop",
        }
    )





@shared_task
def task_buy_apple():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    apple_data = cache.get('apple_key')

    if apple_data:
        apple_quantity = int(apple_data)
        cache.delete('apple_key')
    else:        
        apple_quantity = random.randint(1, 10)

    apple_buy_cost = 4
    apple_cost = apple_buy_cost*apple_quantity
    apple_obj = Commodity.objects.get(raw_title='apple')
    apple_obj.quantity += apple_quantity
    apple_obj.save()
    account_obj = Account.objects.first()
    account_obj.total_debt -= apple_cost
    account_obj.save()

    message = {'change_store': {'apple': apple_obj.quantity},
                'change_account': str(account_obj.total_debt)}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'chat_message',
            'message': message,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task
def task_buy_apple():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    apple_data = cache.get('apple_key')

    if apple_data:
        apple_quantity = int(apple_data)
        cache.delete('apple_key')
    else:        
        apple_quantity = random.randint(1, 10)

    apple_buy_cost = 4
    apple_cost = apple_buy_cost*apple_quantity
    apple_obj = Commodity.objects.get(raw_title='apple')
    apple_obj.quantity += apple_quantity
    apple_obj.save()
    account_obj = Account.objects.first()
    account_obj.total_debt -= apple_cost
    account_obj.save()

    message = {'change_store': {'apple': apple_obj.quantity},
                'change_account': str(account_obj.total_debt)}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'chat_message',
            'message': message,
            "KEY_PREFIX": "fruit_shop",
        }
    )


@shared_task
def task_buy_bannana():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    bannana_data = cache.get('bannana_key')

    if bannana_data:
        bannana_quantity = int(bannana_data)
        cache.delete('bannana_key')
    else:        
        bannana_quantity = random.randint(10, 20)

    bannana_buy_cost = 1
    bannana_cost = bannana_buy_cost*bannana_quantity
    bannana_obj = Commodity.objects.get(raw_title='bannana')
    bannana_obj.quantity += bannana_quantity
    bannana_obj.save()
    account_obj = Account.objects.first()
    account_obj.total_debt -= bannana_cost
    account_obj.save()

    message = {'change_store': {'apple': bannana_obj.quantity},
                'change_account': str(account_obj.total_debt)}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'chat_message',
            'message': message,
            "KEY_PREFIX": "fruit_shop",
        }
    )


@shared_task
def task_buy_peach():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    peach_data = cache.get('peach_key')

    if peach_data:
        peach_quantity = int(peach_data)
        cache.delete('peach_key')
    else:        
        peach_quantity = random.randint(10, 20)

    peach_buy_cost = 1
    peach_cost = peach_buy_cost*peach_quantity
    peach_obj = Commodity.objects.get(raw_title='peach')
    peach_obj.quantity += peach_quantity
    peach_obj.save()
    account_obj = Account.objects.first()
    account_obj.total_debt -= peach_cost
    account_obj.save()

    message = {'change_store': {'apple': peach_obj.quantity},
                'change_account': str(account_obj.total_debt)}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'chat_message',
            'message': message,
            "KEY_PREFIX": "fruit_shop",
        }
    )
