from django.urls import path

# from .consumers import BuyingConsumer, LoginConsumer
from .consumers import BuyingConsumer, ChangeBallanceConsumer

websocket_urlpatterns = [
    path("ws/fruitshop_app/", BuyingConsumer.as_asgi()),
    path("ws/change_ballance/", ChangeBallanceConsumer.as_asgi()),
]