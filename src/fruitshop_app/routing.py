from django.urls import path

# from .consumers import BuyingConsumer, LoginConsumer
from .consumers import BuyingConsumer, ChangeBallanceConsumer,\
                        GetAccountAndLastOperationDataConsumer, ChatWithTechSupport,\
                        AccountAuditConsumer

websocket_urlpatterns = [
    path("ws/fruitshop_app/", BuyingConsumer.as_asgi()),
    path("ws/change_ballance/", ChangeBallanceConsumer.as_asgi()),
    path("ws/get_account_and_last_operaions_data/", GetAccountAndLastOperationDataConsumer.as_asgi()),
    path("ws/chat_with_tech_support/", ChatWithTechSupport.as_asgi()),
    path("ws/get_account_audit/", AccountAuditConsumer.as_asgi()),
]