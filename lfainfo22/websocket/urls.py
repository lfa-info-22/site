
from django.urls import path

from channels.routing import URLRouter
from qcm.websocket.consumers import WSEditorConsumer

ws_urlpatterns = [
    path('qcm/editor', WSEditorConsumer.as_asgi())
]
