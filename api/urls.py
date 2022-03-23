
import importlib
from django.urls import path

from django.conf import settings

urlpatterns = ([

], "api", "api")

def api(cls):
    object = cls()

    urlpatterns[0].append(
        path(f"v{object.VERSION}/{object.APPLICATION}/{object.ROUTE}", object)
    )

    return cls


#
# Load apis (import views that contains api views)
# 
for installed_api in settings.INSTALLED_APIS:
    module = importlib.__import__(installed_api)
