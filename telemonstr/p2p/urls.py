from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/<slug:fiat>/<slug:crypto>/<slug:bank>', binance_dashboard),
    path('dashboard/api/<slug:fiat>/<slug:crypto>/<slug:bank>', binance_dashboard_json),
    path('list/<slug:fiat>/',binance_get_currency_list),
    path('count/<slug:crypto_label>/<slug:fiat_label>/<slug:type>/<slug:payment_method>', test_page),
    path('banks/<slug:fiat>/', binance_bank_list),
    path('bybit/<slug:crypto>/<slug:fiat>/<slug:bank>', bybit_dashboard),
    path('huobi/<slug:crypto>/<slug:fiat>/<slug:bank>', huobi_dashboard),
    path('bestchange/<slug:crypto>/<slug:fiat>/<slug:bank>', bestchange_dashboard),
    path('telegram_send/', p2p_telegram_message)

]