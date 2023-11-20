from django.urls import path

# from .consumers import BuyingConsumer, LoginConsumer
from .consumers import BuyingConsumer, ChangeBallanceConsumer,\
                        GetAccountAndLastOperationDataConsumer

websocket_urlpatterns = [
    path("ws/fruitshop_app/", BuyingConsumer.as_asgi()),
    path("ws/change_ballance/", ChangeBallanceConsumer.as_asgi()),
    path("ws/get_account_and_last_operaions_data/", GetAccountAndLastOperationDataConsumer.as_asgi()),
]