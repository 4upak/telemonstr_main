from django.urls import path
from .views import *

urlpatterns = [

    path('',accounts_main_page),
    path('import/',accounts_import_page, name="import_account_request"),
    path('api/import_accounts',accounts_api_page),
    path('api/active_accounts',active_accounts_api_page),
    path('proxy/',accounts_proxy_page),
    path('proxy/add/',accounts_proxy_add),
    path('proxy/list/',accounts_proxy_list),
    path('proxy/delete/',accounts_proxy_delete),
    path('proxy/check/',accounts_proxy_check),

]