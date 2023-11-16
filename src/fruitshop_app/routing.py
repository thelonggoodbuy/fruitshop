from django.urls import path

from .consumers import BuyingConsumer, LoginConsumer

websocket_urlpatterns = [
    path("ws/fruitshop_app/", BuyingConsumer.as_asgi()),
    path("ws/login/", LoginConsumer.as_asgi()),
]