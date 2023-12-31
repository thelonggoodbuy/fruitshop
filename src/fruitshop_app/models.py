# import django
# django.setup()

from django.db import models
from django.contrib.auth.models import User



# class CustomUser(User):
#     email = models.EmailField()



class Message(models.Model):
    from_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="from_user")
    to_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="to_user")
    message_data_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class Commodity(models.Model):
    raw_title = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(blank=True, null=True)


class TradeOperation(models.Model):
    OPERATION_TYPES_CORT=(("sailing", "продаж"),
                        ("buying", "покупка"))
    TRADE_STATUS_CORT=(("success", "успіх"),
                       ("error", "помилка"))
    trade_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    operation_type = models.CharField(choices=OPERATION_TYPES_CORT)
    status = models.CharField(choices=TRADE_STATUS_CORT)

class Account(models.Model):
    total_debt = models.DecimalField(max_digits=12, decimal_places=2)

class DownloadStatistics(models.Model):
    date = models.DateField(unique=True)
    quantity_of_downloads = models.PositiveIntegerField()