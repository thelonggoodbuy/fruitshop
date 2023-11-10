import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class BuyingConsumer(WebsocketConsumer):
    def connect(self):
        print('Connect work!')
        self.room_name = 'fruit_shop_room'
        self.room_group_name = f"chat_{self.room_name}"
        print('=====Chanel name===========')
        print(self.channel_name)
        print('=====room name============')
        print(self.room_name)
        print('=====Group name============')
        print(self.room_group_name)
        print('===========================')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print('Disconnect work!')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):

        # print('-------------------------')
        # print('Receive work!')
        # print(text_data)
        # print(type(text_data))
        # text_data["message"] = 'smt new'
        # print('-------------------------')
        # text_data_json = json.loads(text_data)

        text_data_json = json.loads(text_data)
        old_value = text_data_json['message']
        text_data_json["message"] = str(int(old_value) + 100)

        message = text_data_json["message"]

        # self.send(text_data=json.dumps({"message": message}))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )