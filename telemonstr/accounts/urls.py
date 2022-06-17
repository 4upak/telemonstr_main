from django.urls import path
from .views import *

urlpatterns = [

    path('',accounts_main_page),
    path('import/',accounts_import_page, name="import_account_request"),
    path('api/import_accounts',accounts_api_page),
    path('api/active_accounts',active_accounts_api_page),
    path('delete/',accounts_delete_active_account)

]