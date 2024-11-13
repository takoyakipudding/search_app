import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path  # URLルーティングに必要
from search_app.consumers import SearchConsumer  # Consumerをインポート

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'search_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/search/', SearchConsumer.as_asgi()),  # ルーティングの定義
        ])
    ),
})
