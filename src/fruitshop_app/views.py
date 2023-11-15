from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import OuterRef, Subquery, CharField
from django.db import models

from .models import Commodity, Account, TradeOperation


# def main_page(request):
#     return render(request, "fruitshop_app/main.html")


class FruitDataListView(TemplateView):
    template_name = "fruitshop_app/main.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["commodity_data"] = Commodity.objects.all().order_by('id')
        context["total_money_in_accout"] = Account.objects.first().total_debt
        context["last_transactions"] = TradeOperation.objects.prefetch_related('commodity').filter().order_by('-id')[:40]
        
        last_date_time_subquery = Subquery(TradeOperation.objects.filter(
            commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
                .values_list('trade_date_time')[:1]
            )
        last_quantity_subquery = Subquery(TradeOperation.objects.filter(
            commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
                .values_list('quantity')[:1]
            )
        last_total_cost_subquery = Subquery(TradeOperation.objects.filter(
            commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
                .values_list('total_cost')[:1]
            )
        last_operation_type_subquery = Subquery(TradeOperation.objects.filter(
            commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
                .values_list('operation_type')[:1]
            )
        
        commodity_last_transaction = Commodity.objects.annotate(last_date_time_quantity=last_date_time_subquery,
                                                                last_quantity=last_quantity_subquery,
                                                                last_total_cost=last_total_cost_subquery,
                                                                last_operation_type=last_operation_type_subquery)\
                                                        .all().order_by('id')
        
        print('-------------------------------')
        print(commodity_last_transaction)
        print('------------------------------')
        
        context["commodity_data"] = commodity_last_transaction

        # print('*****************************')
        # print(commodity_last_transaction)
        # for commodity in  commodity_last_transaction:
        #     print(commodity.__dict__)
        # print('*****************************')



        # context["newest_transactions"] = TradeOperation.objects.prefetch_related('commodity').filter(Commodity)

        # context["last_pineapple_transaction"] = TradeOperation.objects.filter(commodity__title='pineapple').order_by('-id')[:1]
        # context["last_apple_transaction"] = TradeOperation.objects.filter(commodity__title='apple').order_by('-id')[:1]
        # context["last_banana_transaction"] = TradeOperation.objects.filter(commodity__title='apple').order_by('-id')[:1]
        # context["last_orange_transaction"]
        # context["last_peach_transaction"]
        # context["last_kiwi_transaction"]

        return context