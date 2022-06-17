from django.urls import path
from .views import *

urlpatterns = [
    path('', proxy_page),
    path('add/', proxy_add),
    path('list/', proxy_list),
    path('delete/', proxy_delete),
    path('check/', proxy_check),
]