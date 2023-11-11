import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.cache import cache



class BuyingConsumer(WebsocketConsumer):
    def connect(self):
        print('Connect work!')
        self.room_name = 'fruit_shop_room'
        self.room_group_name = f"chat_{self.room_name}"

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

        text_data_json = json.loads(text_data)
        pineapple_value = int(text_data_json['message'])
        cache.set(key='pineapple_key', value=pineapple_value)
        print('(((receive work!))))')


        # text_data_json["message"] = str(int(old_value) + 100)
        # message = text_data_json["message"]



        # async_to_sync(self.channel_layer.group_send)(

        #     self.room_group_name, {"type": "chat.message", "message": message}
        # )


    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))