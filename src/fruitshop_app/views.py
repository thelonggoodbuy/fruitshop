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
        context["commodity_data"] = Commodity.objects.all().order_by('id')
        context["total_money_in_accout"] = Account.objects.first().total_debt
        context["last_transactions"] = TradeOperation.objects.prefetch_related('commodity').filter().order_by('-id')[:40]
        # commodity_dict = Commodity.objects.all()
        # newest = Comment.objects.filter(post=OuterRef('pk')).order_by('-created_at')
        # Post.objects.annotate(newest_commenter_email=Subquery(newest.values('email')[:1]))

        # trade_operation_subquery = Subquery(TradeOperation.objects.filter(
        #     commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
        #         .values('trade_date_time', 'quantity', 'total_cost', 'operation_type')
        #     )
        
        trade_operation_subquery = Subquery(TradeOperation.objects.filter(
            commodity=OuterRef('pk'), status="success").order_by('-trade_date_time')\
                .values_list('quantity', 'trade_date_time')[:1]
            )
        
        commodity_last_transaction = Commodity.objects.annotate(last_trade_quantity=trade_operation_subquery)

        print('*****************************')
        print(commodity_last_transaction)
        for commodity in  commodity_last_transaction:
            print(commodity.__dict__)
        print('*****************************')



        # context["newest_transactions"] = TradeOperation.objects.prefetch_related('commodity').filter(Commodity)

        # context["last_pineapple_transaction"] = TradeOperation.objects.filter(commodity__title='pineapple').order_by('-id')[:1]
        # context["last_apple_transaction"] = TradeOperation.objects.filter(commodity__title='apple').order_by('-id')[:1]
        # context["last_banana_transaction"] = TradeOperation.objects.filter(commodity__title='apple').order_by('-id')[:1]
        # context["last_orange_transaction"]
        # context["last_peach_transaction"]
        # context["last_kiwi_transaction"]

        return context