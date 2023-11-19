from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from django.db.models import OuterRef, Subquery, CharField
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Commodity, Account, TradeOperation
from .forms import LoginForm



class FruitDataListView(LoginView):
    template_name = "fruitshop_app/main.html"
    form_class = LoginForm


    def get_redirect_url(self):
        return reverse_lazy('main_page')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context["commodity_data"] = commodity_last_transaction
        context["form"] = LoginForm()

        return context
    

class FruitShopLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "fruitshop_app/main.html"
    next_page = reverse_lazy('main_page')