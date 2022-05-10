import os

from channels.routing import ProtocolTypeRouter
from channels.http import AsgiHandler
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lfainfo22.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    # Just HTTP for now. (We can add other protocols later.)
})