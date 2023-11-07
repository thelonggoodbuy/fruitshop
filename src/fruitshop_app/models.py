from django.db import models
from django.contrib.auth.models import User



class CustomUser(User):
    pass


class Message(models.Model):
    from_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="from_user")
    to_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="to_user")
    message_data_time = models.DateTimeField()
    text = models.TextField()


class Commodity(models.Model):
    title = models.CharField(max_length=200)
    quantity = models.IntegerField()


class TradeOperations(models.Model):
    OPERATION_TYPES_CORT=(("sailing", "продаж"),
                        ("buying", "покупка"))
    TRADE_STATUS_CORT=(("success", "успіх"),
                       ("error", "помилка"))
    trade_date_time = models.DateTimeField()
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    operation_type = models.CharField(choices=OPERATION_TYPES_CORT)
    status = models.CharField(choices=TRADE_STATUS_CORT)