from django.shortcuts import render
from .models import Bundle, BinanceBudle
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from decimal import Decimal
from datetime import datetime

def trading_dashboard(request):

    data = {'title': "Трейдинг дашборд"}
    return render(request, 'trading.html', context=data)



class TradingBundles(ModelViewSet):
    queryset = Bundle.objects.filter(profitability__gt = 0).order_by('-profitability')[:100]
    serializer_class = BundleSerializer

class TradingBinanceBundles(ModelViewSet):
    queryset = BinanceBudle.objects.all()
    serializer_class = BinanceBundleSerializer

def trading_bundle(request, pk):
    data = {'title': "Связка Детали"}
    return render(request, 'bundle.html', context=data)
