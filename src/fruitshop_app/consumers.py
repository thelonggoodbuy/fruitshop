import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.cache import cache



class BuyingConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'fruit_shop_room'
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def receive(self, text_data):
        received_data_json = json.loads(text_data)
        cache.set(key='changes_in_tasks', value=received_data_json)


    def send_data(self, event):
        data = event["event_data"]
        self.send(text_data=json.dumps({"data": data}))



import pprint
from .tasks import task_change_account_ballance
from channels.auth import UserLazyObject

class ChangeBallanceConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'change_balance_room'
        self.room_group_name = f"chat_{self.room_name}"

        print(f'Chanel_name: {self.channel_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.user = self.scope["user"]
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def receive(self, text_data):
        received_data_json = json.loads(text_data)
        changes_in_account = received_data_json['changes_in_account']

        if self.user.is_authenticated:
            task_change_account_ballance.delay(changes_in_account, self.channel_name)
        else:
            message = 'Щоб змінювати стан банківського рахунку необхідно авторизуватися'
            status = 'fail'
            self.send(text_data=json.dumps({'data': {"message": message, 'status': status}}))


    def send_data(self, event):
        data = event["event_data"]
        self.send(text_data=json.dumps({"data": data}))



class GetAccountAndLastOperationDataConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'fruit_shop_room'
        self.room_group_name = f"account_and_last_operation_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def send_data(self, event):
        data = event["event_data"]
        self.send(text_data=json.dumps({"data": data}))



from faker import Faker
fake = Faker('uk_UA')

from .models import User, Message
from .tasks import task_send_joke
from channels.layers import get_channel_layer
import pprint
# from celery.task.control import revoke
from config.celery import app

class ChatWithTechSupport(WebsocketConsumer):
    chat_chanels_id_set = set()
    task_id = None
    
    def connect(self):
        self.room_name = 'chat_with_techsuport_shop_room'
        self.room_group_name = f"group_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.user = self.scope["user"]

        self.chat_chanels_id_set.add(self.channel_name)


        if len(self.chat_chanels_id_set) == 1:
            task = task_send_joke.delay()
            print(task)
            self.task_id = task.id

        print('-----------CONNECT----CHAT!!!--------------')
        print('--------TASK---------ID--------------------')
        print(self.task_id)
        print(self.chat_chanels_id_set)
        print('-------------------------------------------')

        self.accept()


    def receive(self, text_data):
        print(f'text-data-is: {text_data}')

        received_data_json = json.loads(text_data)

        # chek user status
        if self.user.is_authenticated:
            perm_status = 'authenticated'

            if self.user.last_name == '':
                message_author = self.user.username
            else:
                message_author = self.user.last_name

            response = fake.text(max_nb_chars=40)
            techsuport = User.objects.get(username='techsupport')
            response_author = techsuport.last_name

            Message.objects.create(
                from_user=self.user,
                to_user=techsuport,
                text=received_data_json['message_text']
            )

            Message.objects.create(
                from_user=techsuport,
                to_user=self.user,
                text=response
            )


        else:
            perm_status = 'anonym'
            response = None
            message_author = None
            response_author = None

        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", 
                                   "message": received_data_json,
                                   "message_author": message_author,
                                   "perm_status": perm_status,
                                   "response": response,
                                   "response_author": response_author}
        )



    def disconnect(self, close_code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


        self.chat_chanels_id_set.remove(self.channel_name)
        
        if len(self.chat_chanels_id_set) == 0:
            app.control.revoke(self.task_id, terminate=True, signal='SIGKILL')

        print('----DISCONECT----')
        print(self.chat_chanels_id_set)
        print(len(self.chat_chanels_id_set))
        print(self.task_id)
        print('-----------------')


    def chat_message(self, event):
        data = event
        self.send(text_data=json.dumps({"data": data}))


