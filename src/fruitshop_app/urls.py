from django.urls import path

from .views import FruitDataListView, FruitShopLogoutView, download_declaration


urlpatterns = [
    path("", FruitDataListView.as_view(), name="main_page"),
    path("logout/", FruitShopLogoutView.as_view(), name="logout"),
    path("download_declaration/", download_declaration, name="download_declaration"),
]