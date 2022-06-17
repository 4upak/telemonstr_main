from django.urls import path, re_path


from .consumers import TradingConsumer, StreamingConsumer

websocket_urls = [
    re_path(r"^ws/trading/(?P<start_symbol>[\w-]+)/$", TradingConsumer.as_asgi()),
    re_path(r"^ws/streaming/(?P<symbol>[\w-]+)/$", StreamingConsumer.as_asgi()),
]