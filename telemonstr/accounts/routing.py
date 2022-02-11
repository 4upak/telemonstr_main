from django.urls import path, re_path


from .consumers import AccountsConsumer

websocket_urls = [
    re_path('ˆws/accounts/$', AccountsConsumer.as_asgi()),
    re_path(r"^ws/accounts/(?P<account_id>[\w-]+)/$",AccountsConsumer.as_asgi()),
]