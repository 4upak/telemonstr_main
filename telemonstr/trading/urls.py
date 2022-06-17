from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router = DefaultRouter()
router.register('list', TradingBundles, basename = 'Bundle')
router.register('binancelist', TradingBinanceBundles, basename = 'BinanceBundle')
urlpatterns = router.urls

urlpatterns.append(path('dashboard/', trading_dashboard))
urlpatterns.append(path('bundle/<slug:bundle>/', trading_bundle))