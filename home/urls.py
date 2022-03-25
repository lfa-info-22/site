
from django.urls import path
from home.views  import HomeView, PublicationsView

urlpatterns = ([
    path('', HomeView()),
    path('posts/', PublicationsView())
], "home", "home")
