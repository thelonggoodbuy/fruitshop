from django.urls import path

from .views import FruitDataListView


urlpatterns = [
    path("", FruitDataListView.as_view(), name="main_page"),
]