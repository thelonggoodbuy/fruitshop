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

