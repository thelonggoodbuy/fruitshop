from django.urls import path

from .views import FruitDataListView, FruitShopLogoutView


urlpatterns = [
    path("", FruitDataListView.as_view(), name="main_page"),
    path("logout/", FruitShopLogoutView.as_view(), name="logout"),
]