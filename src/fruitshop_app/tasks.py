from config.celery import app
from celery import shared_task
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache

from django.apps import apps





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

    # how many cost?
    apple_buy_cost = 4
    apple_cost = apple_buy_cost*apple_quantity
    # how many money i have?
    account_obj = Account.objects.first()
    if apple_cost <= account_obj.total_debt:
        apple_obj = Commodity.objects.get(raw_title='apple')
        apple_obj.quantity += apple_quantity
        apple_obj.save()
        account_obj.total_debt -= apple_cost
        account_obj.save()

        output_data = {'change_store': {'apple': apple_obj.quantity},
                        'change_account': str(account_obj.total_debt),
                        'deal_type': 'buying',
                        'fruit_title': apple_obj.title,
                        'fruit_cost': apple_cost,
                        'changed_fruit_quantity': apple_quantity,
                        'message': {'status': 'SUCCESS', 'text':
                            f'Постачальник привіз {apple_quantity} яблук. З рахунку списано {apple_cost}usd. Покупка завершена.'}}
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Постачальник привіз {apple_quantity} яблук. Недостатньо коштів на рахунку. Покупка відмінена.'}}
        
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task
def task_sell_apple():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    apple_data = cache.get('apple_key')

    if apple_data:
        apple_quantity = int(apple_data)
        cache.delete('apple_key')
    else:        
        apple_quantity = random.randint(1, 10)

    # How many apple I have
    apple_obj = Commodity.objects.get(raw_title='apple')
    if apple_obj.quantity >= apple_quantity:

        apple_sell_cost = 5
        apple_cost = apple_sell_cost*apple_quantity
        
        apple_obj.quantity -= apple_quantity
        apple_obj.save()
        account_obj = Account.objects.first()
        account_obj.total_debt += apple_cost
        account_obj.save()

        output_data = {'change_store': {'apple': apple_obj.quantity},
                        'change_account': str(account_obj.total_debt),
                        'deal_type': 'selling',
                        'fruit_title': apple_obj.title,
                        'fruit_cost': apple_cost,
                        'changed_fruit_quantity':apple_quantity,
                        'message': {'status': 'SUCCESS', 'text':
                            f'Покупець придбав {apple_quantity} яблук. На рахунок зараховано {apple_cost}'}}
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Покупець хочу купити {apple_quantity} яблук. Недостатньо товару на складі. Продаж відмінено.'}}
        
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task
def task_buy_banana():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    banana_data = cache.get('banana_key')

    if banana_data:
        banana_quantity = int(banana_data)
        cache.delete('banana_key')
    else:        
        banana_quantity = random.randint(10, 20)

    banana_buy_cost = 1
    banana_cost = banana_buy_cost*banana_quantity
    account_obj = Account.objects.first()
    if banana_cost <= account_obj.total_debt:
        banana_obj = Commodity.objects.get(raw_title='banana')
        banana_obj.quantity += banana_quantity
        banana_obj.save()
        account_obj.total_debt -= banana_cost
        account_obj.save()

        output_data = {'change_store': {'apple': banana_obj.quantity},
                    'change_account': str(account_obj.total_debt),
                    'deal_type': 'buying',
                    'fruit_title': banana_obj.title,
                    'fruit_cost': banana_cost,
                    'changed_fruit_quantity':banana_quantity,
                    'message': {'status': 'SUCCESS', 'text':
                            f'Постачальник привіз {banana_quantity} бананів. З рахунку списано {banana_cost}usd. Покупка завершена.'}}
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Постачальник привіз {banana_quantity} бананів. Недостатньо коштів на рахунку. Покупка відмінена.'}}


    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )




@shared_task
def task_sell_banana():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    banana_data = cache.get('banana_key')

    if banana_data:
        banana_quantity = int(banana_data)
        cache.delete('banana_key')
    else:        
        banana_quantity = random.randint(1, 30)

    banana_obj = Commodity.objects.get(raw_title='banana')

    if banana_obj.quantity >= banana_quantity:

        banana_sell_cost = 2
        banana_cost = banana_sell_cost*banana_quantity
        
        banana_obj.quantity -= banana_quantity
        banana_obj.save()
        account_obj = Account.objects.first()
        account_obj.total_debt += banana_cost
        account_obj.save()

        output_data = {'change_store': {'banana': banana_obj.quantity},
                    'change_account': str(account_obj.total_debt),
                    'deal_type': 'selling',
                    'fruit_title': banana_obj.title,
                    'fruit_cost': banana_cost,
                    'changed_fruit_quantity':banana_quantity,
                    'message': {'status': 'SUCCESS', 'text':
                            f'Покупець придбав {banana_quantity} яблук. На рахунок зараховано {banana_cost}'}}
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Покупець хочу купити {banana_quantity} бананів. Недостатньо товару на складі. Продаж відмінено.'}}
        
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



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
    account_obj = Account.objects.first()
    if pineapple_cost <= account_obj.total_debt:
        pineapple_obj = Commodity.objects.get(raw_title='pineapple')
        pineapple_obj.quantity += pineapple_quantity
        pineapple_obj.save()
        account_obj.total_debt -= pineapple_cost
        account_obj.save()

        output_data = {'change_store': {'pineapple': pineapple_obj.quantity},
                        'change_account': str(account_obj.total_debt),
                        'deal_type': 'buying',
                        'fruit_title': pineapple_obj.title,
                        'fruit_cost': pineapple_cost,
                        'changed_fruit_quantity':pineapple_quantity,
                        'message': {'status': 'SUCCESS', 'text':
                            f'Постачальник привіз {pineapple_quantity} ананасів. З рахунку списано {pineapple_cost}usd. Покупка завершена.'}}
    else:
         output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Постачальник привіз {pineapple_quantity} яблук. Недостатньо коштів на рахунку. Покупка відмінена.'}}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task
def task_sell_pineapple():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    pineapple_data = cache.get('pineapple_key')

    if pineapple_data:
        pineapple_quantity = int(pineapple_data)
        cache.delete('pineapple_key')
    else:        
        pineapple_quantity = random.randint(1, 10)

    pineapple_sell_cost = 4

    pineapple_obj = Commodity.objects.get(raw_title='pineapple')
    if pineapple_obj.quantity >= pineapple_quantity:

        pineapple_cost = pineapple_sell_cost*pineapple_quantity
        
        pineapple_obj.quantity -= pineapple_quantity
        pineapple_obj.save()
        account_obj = Account.objects.first()
        account_obj.total_debt += pineapple_cost
        account_obj.save()

        output_data = {'change_store': {'pineapple': pineapple_obj.quantity},
                        'change_account': str(account_obj.total_debt),
                        'deal_type': 'selling',
                        'fruit_title': pineapple_obj.title,
                        'fruit_cost': pineapple_cost,
                        'changed_fruit_quantity':pineapple_quantity,
                        'message': {'status': 'SUCCESS', 'text':
                            f'Покупець придбав {pineapple_quantity} ананасів. На рахунок зараховано {pineapple_cost}'}}
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Покупець хочу купити {pineapple_quantity} ананасів. Недостатньо товару на складі. Продаж відмінено.'}}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
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
        peach_quantity = random.randint(5, 15)

    peach_buy_cost = 2
    peach_cost = peach_buy_cost*peach_quantity
    account_obj = Account.objects.first()
    if peach_cost <= account_obj.total_debt:
        peach_obj = Commodity.objects.get(raw_title='peach')
        peach_obj.quantity += peach_quantity
        peach_obj.save()
        
        account_obj.total_debt -= peach_cost
        account_obj.save()

        output_data = {'change_store': {'peach': peach_obj.quantity},
                        'change_account': str(account_obj.total_debt),
                        'deal_type': 'buying',
                        'fruit_title': peach_obj.title,
                        'fruit_cost': peach_cost,
                        'changed_fruit_quantity':peach_quantity,
                        'message': {'status': 'SUCCESS', 'text':
                            f'Постачальник привіз {peach_quantity} персиків. З рахунку списано {peach_cost}usd. Покупка завершена.'}}
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Постачальник привіз {peach_quantity} персиків. Недостатньо коштів на рахунку. Покупка відмінена.'}}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task
def task_sell_peach():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')

    peach_data = cache.get('peach_key')

    if peach_data:
        peach_quantity = int(peach_data)
        cache.delete('peach_key')
    else:        
        peach_quantity = random.randint(1, 20)


    peach_obj = Commodity.objects.get(raw_title='peach')
    if peach_obj.quantity >= peach_quantity:

        peach_sell_cost = 3
        peach_cost = peach_sell_cost*peach_quantity
        
        peach_obj.quantity -= peach_quantity
        peach_obj.save()
        account_obj = Account.objects.first()
        account_obj.total_debt += peach_cost
        account_obj.save()

        output_data = {'change_store': {'peach': peach_obj.quantity},
                        'change_account': str(account_obj.total_debt),
                        'deal_type': 'selling',
                        'fruit_title': peach_obj.title,
                        'fruit_cost': peach_cost,
                        'changed_fruit_quantity':peach_quantity,
                        'message': {'status': 'SUCCESS', 'text':
                            f'Покупець придбав {peach_quantity} персиків. На рахунок зараховано {peach_cost}'}}
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Покупець хочу купити {peach_quantity} персиків. Недостатньо товару на складі. Продаж відмінено.'}}


    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



