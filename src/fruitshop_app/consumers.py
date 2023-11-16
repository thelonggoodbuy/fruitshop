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
        print('connect consumer 1')
        self.accept()


    def disconnect(self, close_code):
        print('Disconnect from buying work!')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def receive(self, text_data):
        received_data_json = json.loads(text_data)
        cache.set(key='changes_in_tasks', value=received_data_json)


    def send_data(self, event):
        data = event["event_data"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"data": data}))





class LoginConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = 'fruit_shop_room'
        # self.room_group_name = f"chat_{self.room_name}"

        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )
        print('connect consumer 2')
        print('=====Do you want to login?=======')

        self.accept()

    def disconnect(self, close_code):
        print('Disconnect from login work!')
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )


    def receive(self, text_data):
        authentication_data_json = json.loads(text_data)
        print('----------authentication data from socket-------------')
        print(authentication_data_json)
        print('------------------------------------------------------')
        # cache.set(key='changes_in_tasks', value=received_data_json)
        # print('you_have_receive')
        # print(received_data_json)


    # def send_data(self, event):
    #     data = event["event_data"]
        # Send message to WebSocket
        # self.send(text_data=json.dumps({"data": data}))
