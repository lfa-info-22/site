import os

from channels.routing import ProtocolTypeRouter
from channels.http import AsgiHandler
import django

from channels.routing         import URLRouter
from channels.auth            import AuthMiddlewareStack
from lfainfo22.websocket.urls import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lfainfo22.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns)),
})