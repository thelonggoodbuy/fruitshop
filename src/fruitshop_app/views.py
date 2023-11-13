from django.shortcuts import render
from django.views.generic.base import TemplateView


from .models import Commodity


# def main_page(request):
#     return render(request, "fruitshop_app/main.html")


class FruitDataListView(TemplateView):
    template_name = "fruitshop_app/main.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commodity_data"] = Commodity.objects.all().order_by('id')
        return context