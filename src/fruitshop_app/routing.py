from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/fruitshop_app/", consumers.BuyingConsumer.as_asgi()),
]