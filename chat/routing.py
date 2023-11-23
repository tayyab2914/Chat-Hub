from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sockets-server/(?P<key>\w+)/$', consumers.ChatConsumer.as_asgi())
]