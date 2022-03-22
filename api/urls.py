
from django.urls import path

urlpatterns = ([

], "api", "api")

def api(cls):
    object = cls()

    urlpatterns[0].append(
        path(f"v{object.VERSION}/{object.APPLICATION}/{object.ROUTE}", object)
    )


#
# Load apis (import views that contains api views)
# 
