from django.db import models
import datetime

# Create your models here.
class Bundle(models.Model):
    start_symbol = models.CharField(max_length = 10, null=False, unique=False)
    one_step = models.CharField(max_length = 10, null=False, unique=False)
    two_step = models.CharField(max_length = 10, null=False, unique=False)
    final_step = models.CharField(max_length = 10, null=False, unique=False)
    date = models.DateTimeField(auto_now=True, blank=True)
    profitability = models.DecimalField(max_digits=5,decimal_places=2)

class Stream(models.Model):
    currency = models.CharField(max_length = 10, null=False, unique=True)
    interval = models.CharField(max_length = 10, null=False, unique=True)
    stop = models.IntegerField(default = 0)

class BinancePair(models.Model):
    symbol = models.CharField(max_length = 20, null=False, unique=True)
    base_asset = models.CharField(max_length = 10, null=False, unique=False)
    second_asset = models.CharField(max_length=10, null=False, unique=False)
    last_price = models.DecimalField(max_digits=10,decimal_places=10, default=0)
    date = models.DateTimeField(auto_now=True, blank=True)

class BinanceBudle(models.Model):
    start_stop_symbol = models.CharField(max_length = 20, null=False, default='-')
    first_pair = models.ForeignKey(BinancePair, on_delete=models.PROTECT, related_name='first_pair')
    first_step_symbol = models.CharField(max_length = 20, null=False, default='-')
    second_pair = models.ForeignKey(BinancePair, on_delete=models.PROTECT, related_name='second_pair')
    second_step_symbol = models.CharField(max_length = 20, null=False, default='-')
    third_pair = models.ForeignKey(BinancePair, on_delete=models.PROTECT, related_name='third_pair')