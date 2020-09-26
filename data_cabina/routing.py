from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'api/booth_messages/(?P<booth_token>\w+)/$', consumers.BoothConsumer),
]
