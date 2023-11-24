from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from django.db.models import OuterRef, Subquery, CharField
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Commodity, Account, TradeOperation, Message
from .forms import LoginForm

import pprint

from django.utils.timezone import localtime
import pytz

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
        
        raw_last_messages_data = Message.objects.prefetch_related('from_user').filter().order_by('-id')[:40]

        last_messages_data = []

        # tz = pytz.timezone("Europe/Kiev")

        for message in raw_last_messages_data:
            # print(message.text)
            # utc_datetime = message.message_data_time
            # message.message_data_time = localtime(utc_datetime, tz)
            last_messages_data.insert(0, message)
            # print(f"{message.id}: {message.message_data_time}")

        

        # print('-----------------------------------------------------------------')
        # pprint.pprint(last_messages_data)
        # print('-----------------------------------------------------------------')

        context["last_messages_data"] = last_messages_data
        context["commodity_data"] = commodity_last_transaction
        context["form"] = LoginForm()

        return context
    


class FruitShopLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "fruitshop_app/main.html"
    next_page = reverse_lazy('main_page')



from django.utils import timezone
import pdfkit
from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models import Sum

# from .tasks import task_print_receipt

def download_declaration(request):
    # return task_print_receipt.delay()

    transaction_list = list(TradeOperation.objects.prefetch_related('commodity__title')\
                                                    .filter(trade_date_time__gte=timezone.now().replace(hour=0, minute=0, second=0),
                                                           trade_date_time__lte=timezone.now().replace(hour=23, minute=59, second=59),
                                                           status="success")\
                                                    .values('commodity__title', 'quantity', 'operation_type', 'total_cost', 'trade_date_time'))
    
    for transaciton in transaction_list:
        date_time_new_state = transaciton['trade_date_time'].strftime('%H:%M')
        transaciton['trade_date_time'] = date_time_new_state

    context = {}
    context['transaction_list'] = transaction_list
    transaction_summ = TradeOperation.objects.prefetch_related('commodity__title')\
                                                    .filter(trade_date_time__gte=timezone.now().replace(hour=0, minute=0, second=0),
                                                           trade_date_time__lte=timezone.now().replace(hour=23, minute=59, second=59),
                                                           status="success").aggregate(Sum('total_cost'))
    context['transaction_summ'] = transaction_summ['total_cost__sum']
    template_path = "templates_for_pdf/receipt_template.html"

    prerendered_template = get_template(template_path)

    html = prerendered_template.render(context)
    myPdf = pdfkit.from_string(html, False)
    response = HttpResponse(myPdf, content_type="content_type=application/pdf")

    response[
        "Content-Disposition"
    ] = f"attachment; filename=receipt.pdf"

    return response
