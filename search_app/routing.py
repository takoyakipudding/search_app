from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/search/', consumers.SearchConsumer.as_asgi()),
]
