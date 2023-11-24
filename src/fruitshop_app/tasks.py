from config.celery import app
from celery import shared_task
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache

from django.apps import apps

from django.db.models import OuterRef, Subquery
from django.db.models import F, Func, Value, CharField

from decimal import Decimal

from django.utils import timezone
import pdfkit
from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models import Sum



@shared_task(queue="trade_transaction_task_queue")
def task_buy_apple():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')
    cache_data = cache.get('changes_in_tasks')

    try:
        if cache_data['change_task_apple']['operation_type'] == 'buying' and\
        cache_data['change_task_apple']['commodity_type'] == 'apple':
            apple_quantity = int(cache_data['change_task_apple']['quantity'])
            del cache_data['change_task_apple']
            cache.set('changes_in_tasks', cache_data)
    except KeyError:
        apple_quantity = random.randint(1, 10)
    except TypeError:
        apple_quantity = random.randint(1, 10)

    # how many cost?
    apple_buy_cost = 4
    apple_cost = apple_buy_cost*apple_quantity
    # how many money i have?
    account_obj = Account.objects.first()
    apple_obj = Commodity.objects.get(raw_title='apple')
    if apple_cost <= account_obj.total_debt:
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
        trade_operation = TradeOperation(
            quantity=apple_quantity,
            total_cost=apple_cost,
            operation_type="buying",
            status="success",
        )
        trade_operation.commodity = apple_obj
        trade_operation.save()

    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Постачальник привіз {apple_quantity} яблук. Недостатньо коштів на рахунку. Покупка відмінена.'}}
        trade_operation = TradeOperation(
            operation_type="buying",
            quantity=apple_quantity,
            status="error",
        )
        trade_operation.commodity = apple_obj
        trade_operation.save()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task(queue="trade_transaction_task_queue")
def task_sell_apple():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')
    cache_data = cache.get('changes_in_tasks')


    apple_data = cache.get('apple_key')

    try:
        if cache_data['change_task_apple']['operation_type'] == 'sailing' and\
        cache_data['change_task_apple']['commodity_type'] == 'apple':
            apple_quantity = int(cache_data['change_task_apple']['quantity'])
            del cache_data['change_task_apple']
            cache.set('changes_in_tasks', cache_data)
    except KeyError:
        apple_quantity = random.randint(1, 10)
    except TypeError:
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
        
        trade_operation = TradeOperation(
            quantity=apple_quantity,
            total_cost=apple_cost,
            operation_type="sailing",
            status="success",
        )
        trade_operation.commodity = apple_obj
        trade_operation.save()

    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Покупець хочу купити {apple_quantity} яблук. Недостатньо товару на складі. Продаж відмінено.'}}
        
        trade_operation = TradeOperation(
            quantity=apple_quantity,
            operation_type="sailing",
            status="error",
        )
        trade_operation.commodity = apple_obj
        trade_operation.save()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task(queue="trade_transaction_task_queue")
def task_buy_banana():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')

    cache_data = cache.get('changes_in_banana')
    try:
        if cache_data['change_task_banana']['operation_type'] == 'buying' and\
        cache_data['change_task_banana']['commodity_type'] == 'banana':
            banana_quantity = int(cache_data['change_task_banana']['quantity'])
            del cache_data['change_task_banana']
            cache.set('changes_in_tasks', cache_data)
    except KeyError:
        banana_quantity = random.randint(10, 20)
    except TypeError:
        banana_quantity = random.randint(10, 20)


    banana_buy_cost = 1
    banana_cost = banana_buy_cost*banana_quantity
    account_obj = Account.objects.first()
    banana_obj = Commodity.objects.get(raw_title='banana')
    if banana_cost <= account_obj.total_debt:
        banana_obj.quantity += banana_quantity
        banana_obj.save()
        account_obj.total_debt -= banana_cost
        account_obj.save()

        output_data = {'change_store': {'banana': banana_obj.quantity},
                    'change_account': str(account_obj.total_debt),
                    'deal_type': 'buying',
                    'fruit_title': banana_obj.title,
                    'fruit_cost': banana_cost,
                    'changed_fruit_quantity':banana_quantity,
                    'message': {'status': 'SUCCESS', 'text':
                            f'Постачальник привіз {banana_quantity} бананів. З рахунку списано {banana_cost}usd. Покупка завершена.'}}
        trade_operation = TradeOperation(
            quantity=banana_quantity,
            total_cost=banana_cost,
            operation_type="buying",
            status="success",
        )
        trade_operation.commodity = banana_obj
        trade_operation.save()    
    
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Постачальник привіз {banana_quantity} бананів. Недостатньо коштів на рахунку. Покупка відмінена.'}}
        trade_operation = TradeOperation(
            quantity=banana_quantity,
            operation_type="buying",
            status="error",
        )
        trade_operation.commodity = banana_obj
        trade_operation.save()


    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )




@shared_task(queue="trade_transaction_task_queue")
def task_sell_banana():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')

    cache_data = cache.get('changes_in_banana')
    try:
        if cache_data['change_task_banana']['operation_type'] == 'sailing' and\
        cache_data['change_task_banana']['commodity_type'] == 'banana':
            banana_quantity = int(cache_data['change_task_banana']['quantity'])
            del cache_data['change_task_banana']
            cache.set('changes_in_tasks', cache_data)
    except KeyError:
        banana_quantity = random.randint(1, 30)
    except TypeError:
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
        trade_operation = TradeOperation(
            quantity=banana_quantity,
            total_cost=banana_cost,
            operation_type="sailing",
            status="success",
        )
        trade_operation.commodity = banana_obj
        trade_operation.save()

    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Покупець хочу купити {banana_quantity} бананів. Недостатньо товару на складі. Продаж відмінено.'}}
        trade_operation = TradeOperation(
            quantity=banana_quantity,
            operation_type="sailing",
            status="error",
        )
        trade_operation.commodity = banana_obj
        trade_operation.save()
        
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task(queue="trade_transaction_task_queue")
def task_buy_pineapple():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')

    cache_data = cache.get('changes_in_tasks')

    try:
        if cache_data['change_task_pineapple']['operation_type'] == 'buying' and\
        cache_data['change_task_pineapple']['commodity_type'] == 'pineapple':
            pineapple_quantity = int(cache_data['change_task_pineapple']['quantity'])
            del cache_data['change_task_pineapple']
            cache.set('changes_in_tasks', cache_data)
    except KeyError:
        pineapple_quantity = random.randint(1, 10)
    except TypeError:
        pineapple_quantity = random.randint(1, 10)

    pineapple_buy_cost = 3
    pineapple_cost = pineapple_buy_cost*pineapple_quantity
    account_obj = Account.objects.first()
    pineapple_obj = Commodity.objects.get(raw_title='pineapple')
    if pineapple_cost <= account_obj.total_debt:
        
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
        trade_operation = TradeOperation(
            quantity=pineapple_quantity,
            total_cost=pineapple_cost,
            operation_type="buying",
            status="success",
        )
        trade_operation.commodity = pineapple_obj
        trade_operation.save()
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Постачальник привіз {pineapple_quantity} ананасів. Недостатньо коштів на рахунку. Покупка відмінена.'}}
        trade_operation = TradeOperation(
            quantity=pineapple_quantity,
            operation_type="buying",
            status="error",
        )
        trade_operation.commodity = pineapple_obj
        trade_operation.save()


    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task(queue="trade_transaction_task_queue")
def task_sell_pineapple(queue="trade_transaction_task_queue"):
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')


    cache_data = cache.get('changes_in_tasks')
    try:
        if cache_data['change_task_pineapple']['operation_type'] == 'sailing' and\
        cache_data['change_task_pineapple']['commodity_type'] == 'pineapple':
            pineapple_quantity = int(cache_data['change_task_pineapple']['quantity'])
            del cache_data['change_task_pineapple']
            cache.set('changes_in_tasks', cache_data)
    except KeyError:
        pineapple_quantity = random.randint(1, 10)
    except TypeError:
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
        trade_operation = TradeOperation(
            quantity=pineapple_quantity,
            total_cost=pineapple_cost,
            operation_type="sailing",
            status="success",
        )
        trade_operation.commodity = pineapple_obj
        trade_operation.save()
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Покупець хочу купити {pineapple_quantity} ананасів. Недостатньо товару на складі. Продаж відмінено.'}}
        trade_operation = TradeOperation(
            quantity=pineapple_quantity,
            operation_type="sailing",
            status="error",
        )
        trade_operation.commodity = pineapple_obj
        trade_operation.save()    


    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )



@shared_task(queue="trade_transaction_task_queue")
def task_buy_peach():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')
    cache_data = cache.get('changes_in_tasks')

    try:
        if cache_data['change_task_peach']['operation_type'] == 'buying' and\
        cache_data['change_task_peach']['commodity_type'] == 'peach':
            peach_quantity = int(cache_data['change_task_peach']['quantity'])
            del cache_data['change_task_peach']
            cache.set('changes_in_tasks', cache_data)
    except KeyError:
        peach_quantity = random.randint(5, 15)
    except TypeError:
        peach_quantity = random.randint(5, 15)


    peach_buy_cost = 2
    peach_cost = peach_buy_cost*peach_quantity
    account_obj = Account.objects.first()
    peach_obj = Commodity.objects.get(raw_title='peach')

    if peach_cost <= account_obj.total_debt:
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
        trade_operation = TradeOperation(
            quantity=peach_quantity,
            total_cost=peach_cost,
            operation_type="buying",
            status="success",
        )
        trade_operation.commodity = peach_obj
        trade_operation.save()
    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Постачальник привіз {peach_quantity} персиків. Недостатньо коштів на рахунку. Покупка відмінена.'}}
        trade_operation = TradeOperation(
            operation_type="buying",
            status="error",
        )
        trade_operation.commodity = peach_obj
        trade_operation.save()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )




@shared_task(queue="trade_transaction_task_queue")
def task_sell_peach():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')
    cache_data = cache.get('changes_in_tasks')

    try:
        if cache_data['change_task_peach']['operation_type'] == 'sailing' and\
        cache_data['change_task_peach']['commodity_type'] == 'peach':
            peach_quantity = int(cache_data['change_task_peach']['quantity'])
            del cache_data['change_task_peach']
            cache.set('changes_in_tasks', cache_data)
    except KeyError:
        peach_quantity = random.randint(1, 20)
    except TypeError:
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
        trade_operation = TradeOperation(
            quantity=peach_quantity,
            total_cost=peach_cost,
            operation_type="sailing",
            status="success",
        )
        trade_operation.commodity = peach_obj
        trade_operation.save()

    else:
        output_data = {'change_store': 'null',
                        'change_account': 'null',
                        'message': {'status': 'ERROR', 'text':
                            f'Покупець хочу купити {peach_quantity} персиків. Недостатньо товару на складі. Продаж відмінено.'}}

        trade_operation = TradeOperation(
            quantity=peach_quantity,
            operation_type="sailing",
            status="error",
        )
        trade_operation.commodity = peach_obj
        trade_operation.save()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )


@shared_task(queue="test_second")
def task_foo_bar():
    print('=====123===========>>>>>other queue<<<<<=========456======')
    return None


@shared_task(queue="auxiliary_queue")
def task_change_account_ballance(changes_in_account, channel_name):
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    account_obj = Account.objects.first()
    account_debt_state = account_obj.total_debt
    if changes_in_account['type'] == 'top_up':
        account_obj.total_debt += Decimal(changes_in_account['money'])
        message_text = f"Рахунок поповнено на {changes_in_account['money']} USD"
        status = 'success'
        account_obj.save()
    elif changes_in_account['type'] == 'withdraw' and Decimal(changes_in_account['money']) <= account_debt_state:
        account_obj.total_debt -= Decimal(changes_in_account['money'])
        message_text = f"З рахунку виведено {changes_in_account['money']} USD"
        status = 'success'
        account_obj.save()
    elif changes_in_account['type'] == 'withdraw' and Decimal(changes_in_account['money']) > account_debt_state:
        message_text = f"Поточний стан рахунку не дає змоги вивести з нього {changes_in_account['money']}"
        status = 'fail'

    output_data = {"account_state": str(account_obj.total_debt), "message": message_text, "status": status}

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.send)(
        channel_name,
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )




@shared_task(queue="auxiliary_queue")
def task_update_account_data_and_last_operations():
    Commodity = apps.get_model(app_label='fruitshop_app', model_name='Commodity')
    Account = apps.get_model(app_label='fruitshop_app', model_name='Account')
    TradeOperation = apps.get_model(app_label='fruitshop_app', model_name='TradeOperation')
    account_state = Account.objects.first().total_debt


    last_date_time_subquery = Subquery(TradeOperation.objects.filter(
            commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
                .values_list('trade_date_time')[:1]
            )
    last_quantity_subquery = Subquery(TradeOperation.objects.filter(
        commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
            .values_list('quantity')[:1]
        )
    last_total_cost_subquery = Subquery(TradeOperation.objects.filter(
        commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
            .values_list('total_cost')[:1]
        )
    last_operation_type_subquery = Subquery(TradeOperation.objects.filter(
        commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
            .values_list('operation_type')[:1]
        )
    

    commodity_last_transaction_raw_data = Commodity.objects.annotate(last_date_time_quantity=last_date_time_subquery,
                                                                last_quantity=last_quantity_subquery,
                                                                last_total_cost=last_total_cost_subquery,
                                                                last_operation_type=last_operation_type_subquery)\
                                                            .annotate(format_last_date_time_quantity=Func(
                                                                                                    F('last_date_time_quantity'),
                                                                                                    Value('dd.MM.yyyy hh:mm'),
                                                                                                    function='to_char',
                                                                                                    output_field=CharField()
                                                                                                )
                                                                                            )\
                                                            .all().order_by('id').values(
                                                            'raw_title', 'title', 'format_last_date_time_quantity',
                                                            'last_quantity', 'last_total_cost', 'last_operation_type'
                                                        )
    
    commodity_last_transaction = list(commodity_last_transaction_raw_data)
    
    for commodity in commodity_last_transaction:
        total_cost = commodity['last_total_cost']
        formated_total_cost = str(total_cost)
        commodity['last_total_cost'] = formated_total_cost


    output_data = {"account_state": str(account_state), "commodity_data": commodity_last_transaction}
    
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'account_and_last_operation_fruit_shop_room',
        {
            'type': 'send_data',
            'event_data': output_data,
            "KEY_PREFIX": "fruit_shop",
        }
    )





import httpx
import time
from datetime import datetime

@shared_task(queue="auxiliary_queue")
def task_send_joke(pause=1):

    from django.contrib.auth.models import User
    from django_celery_beat.models import IntervalSchedule, PeriodicTasks, PeriodicTask

    # start_time = time.time()
    Message = apps.get_model(app_label='fruitshop_app', model_name='Message')
    channel_layer = get_channel_layer()
    joker = User.objects.get(username='joker')
    response = httpx.get('https://v2.jokeapi.dev/joke/Any?type=single&contains=cat')
    joke = response.json().get('joke')

    Message.objects.create(
        from_user=joker,
        to_user=None,
        text=joke
    )

    print('-----------JOKES---------------')
    print(joke)
    new_pause = len(joke)
    print(f'Next joke will be after {new_pause} seconds.')

    print('-------------------------------')
    async_to_sync(channel_layer.group_send)(
            "group_chat_with_techsuport_shop_room", 
                {"type": "chat.message", 
                "message": joke,
                "message_author": joker.username,
                "perm_status": "joker",
                "interval": len(joke),
                "response": None,
                "response_author": None}
        )

    time.sleep(new_pause)    
    # finish_time = time.time() - start_time
    
    # print('*********USED TIME WAS**********')
    # print(finish_time)
    # print('********************************')
    task_send_joke(pause=len(joke))
